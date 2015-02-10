#include <Python.h>
#include <gmp.h>

void modinv(mpz_t res, mpz_t a, mpz_t b) {
    
    int ret = mpz_invert (res, a, b);

    if ( ret == 0 ) {   
        mpz_init(res);
    }
}

static PyObject * modinv_wrapper(PyObject * self, PyObject * args)
{
    char * string_a, *string_b;
    mpz_t res, a, b;
    char * result;
    PyObject * ret;
    mpz_init(res);

  // parse arguments
    if (!PyArg_ParseTuple(args, "ss", &string_a, &string_b)) {
        return NULL;
    }

    mpz_init_set_str (a, string_a, 10);	/* Assume decimal integers */
    mpz_init_set_str (b, string_b, 10);

    // run the actual function
    modinv(res, a, b);

    result = malloc(mpz_sizeinbase(res,10)+2);
    mpz_get_str(result, 10, res);
    // build the resulting string into a Python object.
    ret = PyBytes_FromString(result);
    free(result);
    // free(string_a);
    //free(string_b);
    return ret;
}

static PyMethodDef FastToolsMethods[] = {
    { "modinv", modinv_wrapper, METH_VARARGS, "Modular inverse" },
    { NULL, NULL, 0, NULL }
};

//2.7

DL_EXPORT(void) initfasttools(void)
{
  Py_InitModule("fasttools", FastToolsMethods);
} 

//3.2
/*
static struct PyModuleDef fasttoolsmodule = {
   PyModuleDef_HEAD_INIT,
   "fasttools",   // name of module 
   NULL, // module documentation, may be NULL 
   -1,       // size of per-interpreter state of the module,
             //   or -1 if the module keeps state in global variables. 
   FastToolsMethods
};

PyMODINIT_FUNC
PyInit_fasttools(void)
{
    return PyModule_Create(&fasttoolsmodule);
}*/

