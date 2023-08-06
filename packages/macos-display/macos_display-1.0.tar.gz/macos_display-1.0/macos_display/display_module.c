#define PY_SSIZE_T_CLEAN

#include <Python.h>

#include "display.h"

static PyObject* display_name_wrapper(PyObject* module, PyObject* arg)
{
    PyObject *lx;
    if (PyFloat_Check(arg)) {
        double dx = PyFloat_AS_DOUBLE((PyFloatObject *)arg);
        if (!(Py_IS_FINITE(dx) && dx == floor(dx))) {
            PyErr_SetString(PyExc_ValueError,
                            "display_name() only accepts integral values");
            return NULL;
        }
        lx = PyLong_FromDouble(dx);
    }
    else {
        lx = PyNumber_Index(arg);
    }

    if (lx == NULL) {
        return NULL;
    }

    unsigned long x = PyLong_AsUnsignedLong(lx);
    Py_DECREF(lx);
    static unsigned long MAX = 0xffffffff;
    if (x == (((unsigned long) -1) && PyErr_Occurred()) || x > MAX) {
        PyErr_SetString(PyExc_OverflowError, "Can't convert to uint32_t");
        return NULL;
    }

    char* name = getDisplayName((uint32_t) x);
    PyObject* result = PyUnicode_FromString(name);
    free(name);
    if (!result) {
        PyErr_SetString(PyExc_RuntimeError,
                        "Could not decode UTF-8 string response from IOKit");
        return NULL;
    }
    return result;
}

// Our Module's Function Definition struct
// We require this `NULL` to signal the end of our method
// definition
static PyMethodDef methods[] = {
    { "display_name", display_name_wrapper, METH_O, "Gets user-visible display name from display id" },
    { NULL, NULL, 0, NULL }
};

// Our Module Definition struct
static struct PyModuleDef display_module = {
    PyModuleDef_HEAD_INIT,
    "display",
    "macOS display names",
    -1,
    methods

};

// Initializes our module using our above struct
PyMODINIT_FUNC PyInit_display(void)
{
    return PyModule_Create(&display_module
);
}
