# Process this file with Pyrex to produce mpi.c


cdef class MPI_Comm:

    def __init__(MPI_Comm self):
        self.comm = cmpi.MPI_COMM_WORLD


MPI_COMM_WORLD = MPI_Comm()


class MPI_Error(EnvironmentError):
    def __str__(self):
        return MPI_Error_string(self.args[0])


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
