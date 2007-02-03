include $(top_srcdir)/check.am

TESTS = testnemesis

check_PROGRAMS = testnemesis

testnemesis_SOURCES = \
	TestDriver.cc \
	journal/TestDiagnostics.cc \
	test_driver.cc

AM_CPPFLAGS += $(PYTHON_EGG_CPPFLAGS) -I$(PYTHON_INCDIR)

testnemesis_LDADD = \
	-lcppunit -ldl \
	$(PYTHON_BLDLIBRARY) $(PYTHON_LIBS) $(PYTHON_SYSLIBS)


# End of file
