/*
 *~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 *
 *                             nemesis
 *
 * Copyright (c) 2007, California Institute of Technology
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 *
 *    * Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 *
 *    * Redistributions in binary form must reproduce the above
 *    copyright notice, this list of conditions and the following
 *    disclaimer in the documentation and/or other materials provided
 *    with the distribution.
 *
 *    * Neither the name of the California Institute of Technology nor
 *    the names of its contributors may be used to endorse or promote
 *    products derived from this software without specific prior
 *    written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
 * FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
 * COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
 * BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
 * ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 *
 *~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 */ 

/*
 * Python 3.8 introduced a new way (https://peps.python.org/pep-0587/)
 * to initialize the Python interpreter.
 *
 * The previous implementation used here does not work for Python 3.12 and later.
 */

#include <Python.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <mpi.h>

#define COMMAND \
"import sys; " \
"path = sys.argv[1]; " \
"requires = sys.argv[2]; " \
"entry = sys.argv[3]; " \
"path = path.split(':'); " \
"path.extend(sys.path); " \
"sys.path = path; " \
"from pythia.pyre.applications import loadObject; " \
"entry = loadObject(entry); " \
"entry(sys.argv[3:], kwds={'requires': requires})"

/* include the implementation of _mpi */
#include "_mpi.c"

struct _inittab inittab[] = {
    { "_mpi", PyInit__mpi },
    { 0, 0 }
};

int main(int argc, char* argv[])
{
    int c_status;
    PyStatus py_status;
    PyConfig config;
    
#ifdef USE_MPI
    /* initialize MPI */
    if (MPI_Init(&argc, &argv) != MPI_SUCCESS) {
        fprintf(stderr, "%s: MPI_Init failed! Exiting ...", argv[0]);
        return 1;
    }
#endif
    
    /* add our extension module */
    if (PyImport_ExtendInittab(inittab) != 0) {
        fprintf(stderr, "%s: PyImport_ExtendInittab failed! Exiting...\n", argv[0]);
        return 1;
    }

    if (argc < 3 || strcmp(argv[1], "--pythia-start") != 0) {
        PyConfig_InitPythonConfig(&config);
        py_status = PyConfig_SetBytesArgv(&config, argc, argv);
        if (PyStatus_Exception(py_status)) { goto exception; }

        py_status = Py_InitializeFromConfig(&config);
        if (PyStatus_Exception(py_status)) { goto exception; }

        PyConfig_Clear(&config);

        return Py_RunMain();
    } else {
        PyConfig_InitIsolatedConfig(&config);

        py_status = PyConfig_SetBytesString(&config, &config.program_name, argv[0]);
        if (PyStatus_Exception(py_status)) { goto exception; }

        py_status = PyConfig_SetBytesArgv(&config, argc-1, argv+1);
        if (PyStatus_Exception(py_status)) { goto exception; }

        py_status = Py_InitializeFromConfig(&config);
        if (PyStatus_Exception(py_status)) { goto exception; }

        PyConfig_Clear(&config);

        c_status = PyRun_SimpleString(COMMAND);

        Py_FinalizeEx();
    }


#ifdef USE_MPI
    /* shut down MPI */
    MPI_Finalize();
#endif
    
    return c_status;

exception:
    PyConfig_Clear(&config);
    Py_ExitStatusException(py_status);
}

/* end of file */
