dnl -*- Autoconf -*-
dnl Process this file with autoconf to produce a configure script.
dnl

AC_PREREQ(2.59)
AC_INIT([pythia], [1.0.0], [baagaard@usgs.gov])
AC_CONFIG_HEADER([portinfo])
AC_CONFIG_AUX_DIR([./aux-config])
AC_CONFIG_MACRO_DIR([m4])
AM_INIT_AUTOMAKE([foreign subdir-objects tar-pax])

dnl 'configure' options
AC_ARG_VAR(PYTHON, [Python interpreter])
AC_ARG_VAR(PYTHONPATH, [Python module search path])

dnl MPI (build nemesis and mpinemesis: python with MPI)
AC_ARG_ENABLE([mpi],
	[  --enable-mpi        Enable mpi (requires MPI C and C++ compilers) [[default=yes]]],
	[if test "$enableval" = yes ; then enable_mpi=yes; else enable_mpi=no; fi],
	[enable_mpi=yes])
AM_CONDITIONAL([ENABLE_MPI], [test "$enable_mpi" = yes])


dnl TESTING w/cppunit and Python unittest
AC_ARG_ENABLE([testing],
	[  --enable-testing        Enable unit testing with cppunit (requires cppunit) [[default=no]]],
	[if test "$enableval" = yes ; then enable_testing=yes; else enable_testing=no; fi],
	[enable_testing=no])
AM_CONDITIONAL([ENABLE_TESTING], [test "$enable_testing" = yes])

# TEST COVERAGE w/locv and python-coverage
AC_ARG_ENABLE([test-coverage],
	[  --enable-test-coverage  Enable test coverage with lcov and python-coverage [[default=no]]],
	[if test "$enableval" = yes ; then enable_test_coverage=yes; else enable_test_coverage=no; fi],
	[enable_test_coverage=no])
AM_CONDITIONAL([ENABLE_TEST_COVERAGE], [test "$enable_test_coverage" = yes])
AC_ARG_WITH([python-coverage],
    [AC_HELP_STRING([--with-python-coverage],
        [set executable for python-coverage @<:@default=coverage2@:>@])],
	[python_coverage=$withval],
	[python_coverage="coverage2"])
AC_SUBST(python_coverage)

dnl ----------------------------------------------------------------------
dnl CHECK FOR MPI
if test "$enable_mpi" = "yes" ; then
AC_PROG_CC([mpicc hcc mpcc mpcc_r mpxlc cmpicc gcc cc cl icc ecc pgcc xlc xlc_r])
AC_PROG_CXX
AC_SEARCH_LIBS([MPI_Init], [mpi mpich], [], [AC_MSG_ERROR([MPI library not found])])
AC_CHECK_HEADER([mpi.h], [], [AC_MSG_ERROR([header 'mpi.h' not found])])
fi

dnl CHECK FOR C++ compiler
if test "$enable_testing" = "yes"; then
dnl Require C++-11
AX_CXX_COMPILE_STDCXX(11)
fi

AC_PROG_INSTALL

AM_PATH_PYTHON([3.6])
AC_ARG_VAR(PYTHON, [Python interpreter])
AC_ARG_VAR(PYTHONPATH, [Python module search path])
CIT_PYTHON_SYSCONFIG
CIT_CHECK_PYTHON_HEADER
CIT_CHECK_PYTHON_SHARED


dnl ----------------------------------------------------------------------
dnl CPPUNIT
if test "$enable_testing" = "yes" ; then
  CIT_CPPUNIT_HEADER
  CIT_CPPUNIT_LIB
fi

# TEST COVERAGE
if test "$enable_test_coverage" = "yes" ; then
  AC_PATH_PROG(LCOV, lcov)
  if test -z "$LCOV"; then
    AC_MSG_FAILURE([cannot find 'lcov' program for C++ test coverage.])
  fi
  AC_PATH_PROG(PYTHON_COVERAGE, $python_coverage)
  if test -z "$PYTHON_COVERAGE"; then
    AC_MSG_FAILURE([cannot find '$python_coverage' program for Python test coverage.])
  fi
fi


AC_CONFIG_FILES([
  Makefile
  nemesis/Makefile
  bin/Makefile
  libsrc/Makefile
  libsrc/pythia/Makefile
  tests/Makefile
  tests/pytests/Makefile
  tests/libtests/Makefile
])

AC_OUTPUT

dnl end of configure.ac
