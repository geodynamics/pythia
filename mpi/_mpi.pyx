# Process this file with Pyrex to produce mpi.c


cimport cmpi


cdef extern from "stdlib.h":
    void *malloc(int)
    void free(void *)


cdef class MPI_Comm:

    cdef cmpi.MPI_Comm comm

    def __init__(MPI_Comm self):
        self.comm = cmpi.MPI_COMM_WORLD


MPI_COMM_WORLD = MPI_Comm()


class MPI_Error(EnvironmentError):
    def __str__(self):
        return MPI_Error_string(self.args[0])


def MPI_Init(argv):
    cdef int error, cargc, i
    cdef char **cargv, **mycargv
    myargv = []

    # Construct a C char** argument vector from 'argv'.
    cargc = len(argv)
    cargv = <char **>malloc((cargc + 1) * sizeof(char *))
    for i from 0 <= i < cargc:
        arg = argv[i]
        myargv.append(arg) # add ref
        cargv[i] = arg
    cargv[cargc] = NULL

    # Call MPI_Init().
    mycargv = cargv; # MPI might allocate & return its own.
    error = cmpi.MPI_Init(&cargc, &cargv)
    if error != cmpi.MPI_SUCCESS:
        free(mycargv)
        raise MPI_Error(error)

    # Reconstruct Python's 'argv' from the modified 'cargv'.
    del argv[:]
    for i from 0 <= i < cargc:
        argv.append(cargv[i])
    free(mycargv)
    
    return


def MPI_Finalize():
    cdef int error
    error = cmpi.MPI_Finalize()
    if error != cmpi.MPI_SUCCESS:
        raise MPI_Error(error)
    return


def MPI_Comm_rank(comm):
    cdef int error
    cdef int rank
    cdef MPI_Comm c_comm
    c_comm = comm
    error = cmpi.MPI_Comm_rank(c_comm.comm, &rank)
    if error != cmpi.MPI_SUCCESS:
        raise MPI_Error(error)
    return rank


def MPI_Comm_size(comm):
    cdef int error
    cdef int size
    cdef MPI_Comm c_comm
    c_comm = comm
    error = cmpi.MPI_Comm_size(c_comm.comm, &size)
    if error != cmpi.MPI_SUCCESS:
        raise MPI_Error(error)
    return size


cdef char cstring[1024]

def MPI_Error_string(int errorcode):
    cdef int error
    cdef int resultlen
    error = cmpi.MPI_Error_string(errorcode, cstring, &resultlen)
    if error != cmpi.MPI_SUCCESS:
        raise MPI_Error(error)
    if resultlen >= 1024:
        raise RuntimeError("buffer overflow")
    string = cstring
    return string
    

# end of file
