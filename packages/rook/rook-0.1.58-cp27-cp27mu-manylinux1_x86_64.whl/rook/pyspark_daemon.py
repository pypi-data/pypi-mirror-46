"""
Loads Rook into pyspark workers
Usage: spark-submit --conf spark.python.daemon.module=rook.pyspark_daemon
"""
import types
import pyspark.daemon
import functools
import six
import sys
import os
import itertools

original_worker_main = pyspark.daemon.worker_main


def worker_main(*args, **kwargs):
    try:
        import rook
        rook.start(log_file="", log_to_stderr=True)
        from rook.logger import logger
        logger.debug("Started Rook in Spark worker")
        from rook.interface import _rook as singleton, _TRUE_VALUES
        from rook.services import ImportService
        import_service = singleton.get_trigger_services().get_service(ImportService.NAME)

        def pickle_load_hook(orig_func, *args, **kwargs):
            obj = orig_func(*args, **kwargs)
            try:
                if os.environ.get("ROOKOUT_ROOK_EXPERIMENTAL_ENABLE_PYSPARK_CODE_OBJECT_CRAWLING", "False") in _TRUE_VALUES:
                    functions = []
                    if isinstance(obj, tuple):
                        functions = [func for func in obj[:4] if isinstance(func, types.FunctionType)]
                    from rook.services.exts.cloud_debug_python.module_explorer import _GetModuleCodeObjects
                    code_objs = []
                    for function in functions:
                        code_objs = itertools.chain(code_objs, _GetModuleCodeObjects(function))
                    for code_obj in code_objs:
                        import_service._notify_of_pickled_code_object(os.path.splitext(code_obj.co_filename)[0],
                                                                      code_obj.co_filename,
                                                                      code_obj)
                import_service.evaluate_module_list()
            except:
                logger.exception("Silenced exception during module list evaluation")
            return obj

        # we may end up missing pickle module imports if we rely on the sys.modules polling thread
        import pyspark.serializers
        pyspark.serializers.pickle.loads = functools.partial(pickle_load_hook, pyspark.serializers.pickle.loads)
        pyspark.serializers.pickle.load = functools.partial(pickle_load_hook, pyspark.serializers.pickle.load)
    except:
        six.print_("Starting Rook in worker_main failed", file=sys.stderr)

    result = original_worker_main(*args, **kwargs)
    return result


pyspark.daemon.worker_main = worker_main

if __name__ == '__main__':
    pyspark.daemon.manager()
