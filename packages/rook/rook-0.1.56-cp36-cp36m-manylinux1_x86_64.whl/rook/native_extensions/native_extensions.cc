#include "native_extensions.h"
#include "atfork.h"

namespace native_extensions{

PyObject* Module;

static PyMethodDef g_native_extensions_functions[] = {
  {
    "RegisterPreforkCallback",
    RegisterPreforkCallback,
    METH_VARARGS,
    "Registers to the pre fork callback to print the user that we do not support forking"
  },
  { nullptr, nullptr, 0, nullptr }  // sentinel
};

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef moduledef = {
  PyModuleDef_HEAD_INIT, /** m_base */
  NATIVE_EXTENSION_MODULE_NAME, /** m_name */
  "Rookout native extensions", /** m_doc */
  -1, /** m_size */
  g_native_extensions_functions, /** m_methods */
  NULL, /** m_slots */
  NULL, /** m_traverse */
  NULL, /** m_clear */
  NULL /** m_free */
};

PyObject* InitNativeExtensionModuleInternal() {
      Module = PyModule_Create(&moduledef);
#else
PyObject* InitNativeExtensionModuleInternal() {
  Module = Py_InitModule3(
      NATIVE_EXTENSION_MODULE_NAME,
      g_native_extensions_functions,
      "Rookout native extensions");
#endif

  return Module;
}



void InitNativeExtensions() {
    InitNativeExtensionModuleInternal();
}
}  // namespace native_extensions

// This function is called to initialize the module.
#if PY_MAJOR_VERSION >= 3
PyMODINIT_FUNC PyInit_native_extensions() {
  return native_extensions::InitNativeExtensionModuleInternal();
}
#else
PyMODINIT_FUNC initnative_extensions() {
  native_extensions::InitNativeExtensions();
}
#endif
