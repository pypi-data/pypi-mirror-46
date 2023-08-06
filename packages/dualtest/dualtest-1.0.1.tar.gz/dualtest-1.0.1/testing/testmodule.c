#include<Python.h>


static PyObject* testmodule_testmethod(PyObject* self, PyObject* args)
{
    Py_RETURN_TRUE;
}


static PyMethodDef testmodule_methods[] = {
    {"testmethod", testmodule_testmethod, METH_NOARGS, NULL},
    {NULL}
};

static PyModuleDef testmodule = {
    PyModuleDef_HEAD_INIT,
    "testmodule",
    NULL,
    0,
    testmodule_methods,
};

PyMODINIT_FUNC PyInit_testmodule(void)
{
    PyObject* module = PyModule_Create(&testmodule);
    return module;
}
