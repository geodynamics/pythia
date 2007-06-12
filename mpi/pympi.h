/* 
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// 
//                        California Institute of Technology
//                          (C) 2006  All Rights Reserved
// 
//  <LicenseText>
// 
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/ 

#if !defined(mpi_pympi_h)
#define mpi_pympi_h


#include <mpi.h>
#include <Python.h>


#ifdef __cplusplus
extern "C" {
#endif

    typedef struct {
        PyObject_HEAD
        MPI_Comm comm;
    } PyMPICommObject;

    typedef struct {
        PyObject_HEAD
        MPI_Group group;
    } PyMPIGroupObject;

#ifdef __cplusplus
}
#endif


#endif /* mpi_pympi_h */

/* end of file */
