#include "Python.h"

#ifdef Py_XSETREF
#define BUILDING_FOR_CPYTHON 1
#endif

namespace native_extensions {
  extern PyObject* Module;
}
