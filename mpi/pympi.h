// 
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// 
//                        California Institute of Technology
//                          (C) 2006  All Rights Reserved
// 
//  <LicenseText>
// 
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// 

#if !defined(mpi_pympi_h)
#define mpi_pympi_h


#include <mpi.h>
#include <Python.h>


#ifdef __cplusplus
extern "C" {
#endif

    struct PyMPICommObject {
        PyObject_HEAD
        MPI_Comm comm;
    };

#ifdef __cplusplus
}
#endif


#endif /* mpi_pympi_h */

/* end of file */
