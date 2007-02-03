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
#include "pythia/mpi/_mpi.c"

struct _inittab inittab[] = {
    { "_mpi", PyInit__mpi },
    { 0, 0 }
};


void
freeWchar(wchar_t** strings,
	  const int nstrings) {
  for (int i = 0; i < nstrings; ++i) {
    PyMem_RawFree(strings[i]);
  }
  PyMem_Del(strings);
} 
  

wchar_t**
wcharFromChar(char* strings[],
	      const int nstrings) {
  wchar_t** wstrings = PyMem_New(wchar_t*, nstrings);
  if (!wstrings) {
    return NULL;
  }

  for (int i = 0; i < nstrings; ++i) {
    wstrings[i] = Py_DecodeLocale(strings[i], NULL);
    if (!wstrings[i]) {
      freeWchar(wstrings, i);
      return NULL;
    }
  }

  return wstrings;
}


int main(int argc, char* argv[])
{
    int status;
    
#ifdef USE_MPI
    /* initialize MPI */
    if (MPI_Init(&argc, &argv) != MPI_SUCCESS) {
        fprintf(stderr, "%s: MPI_Init failed! Exiting ...", argv[0]);
        return 1;
    }
#endif
    
    /* add our extension module */
    if (PyImport_ExtendInittab(inittab) == -1) {
        fprintf(stderr, "%s: PyImport_ExtendInittab failed! Exiting...\n", argv[0]);
        return 1;
    }

    wchar_t** _argv = wcharFromChar(argv, argc);
    if (!_argv) {
        fprintf(stderr, "%s: Decoding argv strings failed! Exiting...\n", argv[0]);
        return 1;
    }
    
    if (argc < 3 || strcmp(argv[1], "--pythia-start") != 0) {
      status = Py_Main(argc, _argv);
      freeWchar(_argv, argc);
      return status;
    }
    
    /* make sure 'sys.executable' is set to the path of this program  */
    Py_SetProgramName(_argv[0]);
    
    /* initialize Python */
    Py_Initialize();
    
    /* initialize sys.argv */
    PySys_SetArgv(argc - 1, _argv + 1);

    freeWchar(_argv, argc);
    
    /* run the Python command */
    status = PyRun_SimpleString(COMMAND) != 0;
    
    /* shut down Python */
    Py_FinalizeEx();
    
#ifdef USE_MPI
    /* shut down MPI */
    MPI_Finalize();
#endif
    
    return status;
}

/* end of file */
