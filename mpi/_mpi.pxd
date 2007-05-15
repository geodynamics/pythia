# private Pyrex/C interface ~ prefer "cimport mpi" to "cimport _mpi"


cimport cmpi


cdef class MPI_Comm:

    cdef cmpi.MPI_Comm comm


# end of file
