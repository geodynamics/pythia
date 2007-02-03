dnl                                               -*- Autoconf -*-
dnl Process this file with autoconf to produce a configure script.
dnl

AC_PREREQ(2.59)
AC_INIT([nemesis], [2.0.0], [baagaard@usgs.gov])
AC_CONFIG_HEADER([portinfo])
AC_CONFIG_AUX_DIR([./aux-config])
AC_CONFIG_MACRO_DIR([m4])
AM_INIT_AUTOMAKE([foreign subdir-objects tar-pax])

# 'configure' options
AC_ARG_VAR(PYTHON, [Python interpreter])
AC_ARG_VAR(PYTHONPATH, [Python module search path])

# TESTING w/cppunit and Python unittest
AC_ARG_ENABLE([testing],
	[  --enable-testing        Enable unit testing with cppunit (requires cppunit) [[default=no]]],
	[if test "$enableval" = yes ; then enable_testing=yes; else enable_testing=no; fi],
	[enable_testing=no])
AM_CONDITIONAL([ENABLE_TESTING], [test "$enable_testing" = yes])

# ----------------------------------------------------------------------
AC_PROG_CXX
AC_PROG_CC([mpicc hcc mpcc mpcc_r mpxlc cmpicc gcc cc cl icc ecc pgcc xlc xlc_r])
AC_PROG_LIBTOOL
AC_PROG_INSTALL

# Require C++-11
AX_CXX_COMPILE_STDCXX(11)

AM_PATH_PYTHON([3.6])
AC_ARG_VAR(PYTHON, [Python interpreter])
AC_ARG_VAR(PYTHONPATH, [Python module search path])
CIT_PYTHON_SYSCONFIG
CIT_CHECK_PYTHON_HEADER
CIT_CHECK_PYTHON_SHARED

# Check for pythia (which includes mpi).
CIT_PYTHON_MODULE([pythia],[0.9.0])

# Add pythia path to PYTHON_EGG_CPPFLAGS
eval p=`$PYTHON -c "import pythia; print(pythia.__""file__.replace('pythia/__init__.py',''))"`
PYTHON_EGG_CPPFLAGS="-I$p"
AC_SUBST(PYTHON_EGG_CPPFLAGS)

# Checks for libraries.
AC_SEARCH_LIBS([MPI_Init], [mpi mpich], [], [AC_MSG_ERROR([MPI library not found])])

# Checks for header files.
AC_CHECK_HEADER([mpi.h], [], [AC_MSG_ERROR([header 'mpi.h' not found])])

# ----------------------------------------------------------------------
# CPPUNIT
if test "$enable_testing" = "yes" ; then
  CIT_CPPUNIT_HEADER
  CIT_CPPUNIT_LIB
fi

AC_CONFIG_FILES([
  Makefile
  src/Makefile
  tests/Makefile
  tests/pytests/Makefile
  tests/libtests/Makefile
])

AC_OUTPUT

dnl end of configure.ac
