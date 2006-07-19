// -*- C++ -*-
// 
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// 
//                               Michael A.G. Aivazis
//                        California Institute of Technology
//                        (C) 1998-2005 All Rights Reserved
// 
//  <LicenseText>
// 
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// 

#if !defined(pympi__mpimodule_h__)
#define pympi__mpimodule_h__

#include <mpi.h>
#include <Python.h>

#if !defined(pympi_Communicator_h__)
#include "Communicator.h"
#endif


namespace mpi {
    
    class _mpimodule;
    
}


class mpi::_mpimodule {

// meta-methods
public:
    
    _mpimodule() {
        PyImport_AppendInittab("_mpi", &init_mpi);
    }
    
    ~_mpimodule() {}
    
private:
    static inline void init_mpi();
    
    static PyObject * communicatorRank(PyObject *, PyObject * args) {
        PyObject * py_comm;
        if (!PyArg_ParseTuple(args, "O:communicatorRank", &py_comm)) return 0;
        Communicator * comm = (Communicator *) PyCObject_AsVoidPtr(py_comm);
        return PyInt_FromLong(comm->rank());
    }
    
    static PyObject * communicatorSize(PyObject *, PyObject * args) {
        PyObject * py_comm;
        if (!PyArg_ParseTuple(args, "O:communicatorSize", &py_comm)) return 0;
        Communicator * comm = (Communicator *) PyCObject_AsVoidPtr(py_comm);
        return PyInt_FromLong(comm->size());
    }
    
};


inline void mpi::_mpimodule::init_mpi()
{
    static struct PyMethodDef _methods[] = {
        {"communicatorRank", communicatorRank, METH_VARARGS, ""},
        {"communicatorSize", communicatorSize, METH_VARARGS, ""},
        {0, 0}
    };

    // create the module and add the functions
    PyObject * m = Py_InitModule4(
        "_mpi", _methods, "", 0, PYTHON_API_VERSION);

    // get its dictionary
    PyObject * d = PyModule_GetDict(m);

    // check for errors
    if (PyErr_Occurred()) {
        Py_FatalError("can't initialize module _mpi");
    }

    // install the module exceptions
    PyObject *pympi_runtimeError = PyErr_NewException("mpi.runtime", 0, 0);
    PyDict_SetItemString(d, "RuntimeException", pympi_runtimeError);

    // add some constants
    PyDict_SetItemString(d, "initialized", PyLong_FromLong(1));
    PyDict_SetItemString(
        d, "world", PyCObject_FromVoidPtr(new mpi::Communicator(MPI_COMM_WORLD), 0));

    return;
}


namespace mpi {
    static _mpimodule _mpimodule;
}


// version
// $Id: _mpimodule.cc,v 1.1.1.1 2005/03/08 16:13:30 aivazis Exp $

#endif

// End of file
