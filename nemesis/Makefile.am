bin_PROGRAMS = nemesis mpinemesis

AM_CPPFLAGS = $(PYTHON_EGG_CPPFLAGS) $(PYTHON_CPPFLAGS)
AM_LDFLAGS = $(PYTHON_LDFLAGS)
LIBS = $(PYTHON_LIBS)

# nemesis (links MPI, but does not initialize it)
nemesis_SOURCES = nemesis.c

# mpinemesis (initializes MPI before starting Python)
mpinemesis_SOURCES = nemesis.c
mpinemesis_CFLAGS = -DUSE_MPI

EXTRA_DIST = \
    _mpi.c \
    _mpi.pxd \
    _mpi.pyx \
    cmpi.pxd \
    mpi.pxd \
    pympi.h

# End of file
