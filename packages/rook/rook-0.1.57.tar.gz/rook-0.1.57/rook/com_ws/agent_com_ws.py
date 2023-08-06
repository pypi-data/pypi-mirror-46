import sys
import atexit
import uuid
import threading
import functools
import time

from tornado.ioloop import IOLoop
from tornado import gen
from tornado.websocket import websocket_connect, WebSocketClosedError
from tornado.httpclient import HTTPRequest
from tornado.concurrent import Future

try:
    from tornado.concurrent import future_set_result_unless_cancelled
except ImportError:
    def future_set_result_unless_cancelled(future, result):
        if not future.cancelled():
            future.set_result(result)

try:
    from tornado.httpclient import HTTPClientError
except ImportError:
    from tornado.httpclient import HTTPError as HTTPClientError

try:
    from tornado.concurrent import future_set_exc_info
except ImportError:
    def future_set_exc_info(future, exc_info):
        future.set_exc_info(exc_info)

from rook.com_ws import information
from rook.logger import logger
import rook.protobuf2.messages_pb2 as messages_pb
import rook.protobuf2.envelope_pb2 as envelope_pb
from rook.config import AgentComConfiguration, VersionConfiguration
from rook.exceptions import RookCommunicationException, RookInvalidToken


def wrap_in_envelope(message):
    envelope = envelope_pb.Envelope()
    envelope.timestamp.GetCurrentTime()
    envelope.msg.Pack(message)

    return envelope


class CancelledError(Exception):
    pass


class CancellationToken(object):
    def __init__(self):
        self._cancelled = False
        self._callbacks = []
        self._children = []

    def child(self):
        t = CancellationToken()
        self._children.append(t)
        return t

    def cancel(self):
        self._cancelled = True

        for child in self._children:
            child.cancel()

        for f, args, kwargs in self._callbacks:
            try:
                f(*args, **kwargs)
            except Exception:
                pass

    def cancelled(self):
        return self._cancelled

    def register_callback(self, f, *args, **kwargs):
        if self.cancelled():
            f(*args, **kwargs)
            return

        self._callbacks.append((f, args, kwargs))


class _NullCancellationToken(CancellationToken):
    def child(self): return self

    def cancel(self): pass

    def cancelled(self): return False

    def register_callback(self, f, *args, **kwargs): pass


NullCancellationToken = _NullCancellationToken()


class Queue(object):
    def __init__(self):
        import collections

        self._q = collections.deque()
        self._getters = collections.deque()

    def _push(self, item, pusher):
        pusher(item)

        while self._getters:
            future, cancel = self._getters.pop()

            if not future.cancelled() and not cancel.cancelled():
                future.set_result(self._q.pop())
                break

    def push_front(self, item):
        self._push(item, self._q.append)

    def push_back(self, item):
        self._push(item, self._q.appendleft)

    def pop(self, cancel=NullCancellationToken):
        future = Future()

        if self._q:
            future_set_result_unless_cancelled(future, self._q.pop())
            return future

        def cb(f):
            try:
                raise CancelledError()
            except CancelledError:
                future_set_exc_info(f, sys.exc_info())

        child_cancel = cancel.child()
        child_cancel.register_callback(cb, future)

        self._getters.appendleft((future, cancel))

        return future


class MessageCallback(object):
    def __init__(self, cb, persistent):
        self.cb = cb
        self.persistent = persistent


class AgentCom(object):
    def __init__(self, host, port, token, labels, tags):
        self._thread = threading.Thread(name="rookout-" + type(self).__name__, target=self._thread_func)
        self._thread.daemon = True

        self._host = host
        self._port = port
        self._token = token
        self._labels = labels or {}
        self._tags = tags or []
        self._reset_id()

        self._loop = None
        self._connection = None
        self._queue = Queue()
        self._cancel = CancellationToken()

        self._running = True

        self._ready_event = threading.Event()
        self._connection_error = None

        self._callbacks = {}

        def set_ready_event(*args):
            self._ready_event.set()

        self.once('InitialAugsCommand', set_ready_event)

        atexit.register(self.stop)

    def start(self):
        self._thread.start()

    def stop(self):
        self._running = False

        def cb():
            self._cancel.cancel()

            if self._connection is not None:
                self._connection.close(1000)

            self._loop.stop()

        self._loop.add_callback(cb)

    def add(self, message):
        def f():
            envelope = wrap_in_envelope(message)
            self._queue.push_back(envelope)
        self._loop.add_callback(f)

    def on(self, message_name, callback):
        self._register_callback(message_name, MessageCallback(callback, True))

    def once(self, message_name, callback):
        self._register_callback(message_name, MessageCallback(callback, False))

    def await_message(self, message_name):
        def callback(f, message):
            future_set_result_unless_cancelled(f, None)

        future = Future()
        self.once(message_name, functools.partial(callback, future))

        return future

    def wait_for_ready(self, timeout=None):
        if not self._ready_event.wait(timeout):
            raise RookCommunicationException()
        else:
            if self._connection_error is not None:
                raise self._connection_error

    def _thread_func(self):
        self._loop = IOLoop()

        self._loop.add_callback(self._connect)
        self._loop.start()

    @gen.coroutine
    def _connect(self):
        retry = 0
        backoff = AgentComConfiguration.BACK_OFF
        connected = False
        last_successful_connection = 0

        while not self._cancel.cancelled():
            try:
                try:
                    if connected and time.time() >= last_successful_connection + AgentComConfiguration.WS_RESET_BACKOFF_TIMEOUT:
                        retry = 0
                        backoff = AgentComConfiguration.BACK_OFF

                    self._connection = yield self._create_connection()
                    yield self._register_agent()
                except HTTPClientError as e:
                    if e.code == 403:
                        self._connection_error = RookInvalidToken()
                        self._ready_event.set()
                        return
                    else:
                        raise
            except Exception as e:
                retry += 1
                backoff = min(backoff * 2, AgentComConfiguration.MAX_SLEEP)
                connected = False

                reason = str(e)
                if hasattr(e, 'message'):
                    reason = e.message
                logger.info('Connection failed; reason = %s, retry = #%d, waiting %.3fs', reason, retry, backoff)

                yield gen.sleep(backoff)
                continue
            else:
                connected = True
                last_successful_connection = time.time()

            cancel = self._cancel.child()

            routines = [self._incoming(cancel)]
            yield self.await_message('InitialAugsCommand')

            routines.append(self._outgoing(cancel))

            wait_iter = gen.WaitIterator(*routines)

            try:
                yield wait_iter.next()
            except Exception as e:
                logger.error("Coroutine failed with error: %s", e)

            cancel.cancel()

            yield gen.multi(routines)

    @gen.coroutine
    def _incoming(self, cancel):
        while not cancel.cancelled():
            msg = yield self._connection.read_message()

            if msg is None:
                # socket disconnected
                break

            envelope = envelope_pb.Envelope()
            envelope.ParseFromString(msg)
            self._handle_incoming_message(envelope)

    @gen.coroutine
    def _outgoing(self, cancel):
        while not cancel.cancelled():
            msg = None

            try:
                msg = yield self._queue.pop(cancel)
                f = self._send(msg)

                msg = yield f
            except (WebSocketClosedError, CancelledError):
                if msg is not None:
                    self._queue.push_front(msg)

    def _create_connection(self):
        request = HTTPRequest('{}:{}/v1'.format(self._host, self._port))
        request.user_agent = 'RookoutAgent/{}+{}'.format(VersionConfiguration.VERSION, VersionConfiguration.COMMIT)
        request.connect_timeout = AgentComConfiguration.WS_CONNECT_TIMEOUT

        if self._token is not None:
            request.headers["X-Rookout-Token"] = self._token

        return websocket_connect(request,
                                 ping_interval=AgentComConfiguration.WS_PING_INTERVAL,
                                 ping_timeout=AgentComConfiguration.WS_PING_TIMEOUT)

    @gen.coroutine
    def _register_agent(self):
        info = information.collect()
        info.agent_id = self.id
        info.labels = self._labels
        info.tags = self._tags

        m = messages_pb.NewAgentMessage()
        m.agent_info.CopyFrom(information.pack_agent_info(info))

        return self._send(wrap_in_envelope(m))

    AcceptedMessageTypes = [
        messages_pb.InitialAugsCommand,
        messages_pb.AddAugCommand,
        messages_pb.ClearAugsCommand,
        messages_pb.PingMessage,
        messages_pb.RemoveAugCommand
    ]

    def _handle_incoming_message(self, envelope):
        for message_type in self.AcceptedMessageTypes:
            if envelope.msg.Is(message_type.DESCRIPTOR):
                message = message_type()
                envelope.msg.Unpack(message)
                type_name = message.DESCRIPTOR.name

                callbacks = self._callbacks.get(type_name)

                if callbacks:
                    remaining_callbacks = []

                    for callback in callbacks:
                        try:
                            callback.cb(message)
                        except Exception:
                            pass
                        finally:
                            if callback.persistent:
                                remaining_callbacks.append(callback)

                    self._callbacks[type_name] = remaining_callbacks

    def _send(self, message):
        return self._connection.write_message(message.SerializeToString(), binary=True)

    def _register_callback(self, message_name, callback):
        self._callbacks.setdefault(message_name, []).append(callback)

    def _reset_id(self):
        self.id = uuid.uuid4().hex
