// Ensure that Python.h is included before any other header.
#include "common.h"

#ifdef BUILDING_FOR_CPYTHON
namespace native_extensions {

PyObject* CallImportHookRemovingFrames(PyObject* self, PyObject* args, PyObject* kwargs);

PyObject* SetImportHook(PyObject* self, PyObject* hook);

PyObject* SetRemoveImportHookFrames(PyObject* self, PyObject* enabled);

}  // namespace native_extensions
#endif