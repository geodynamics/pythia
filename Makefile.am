ACLOCAL_AMFLAGS = -I m4

SUBDIRS = \
	bin \
	libsrc \
	pythia

if ENABLE_MPI
  SUBDIRS += nemesis
endif


if ENABLE_TESTING
  SUBDIRS += tests
endif

EXTRA_DIST = \
	AUTHORS \
	COPYING \
	NEWS \
	README.md \
	CHANGES.md \
	setup.py \
	setup.cfg \
	configure.ac \
	docker/builder.py \
	docker/debian-stable \
	docker/debian-testing \
	docker/ubuntu-18.04 \
	docker/ubuntu-20.04 \
	docker/ubuntu-22.04 \
	docker/fedora-34 \
	docker/fedora-35 \
	docker/fedora-36 \
	docker/rockylinux-8 \
	docker/pythia-testenv \
	developer/uncrustify.cfg \
	ci-config/run_tests.sh \
	ci-config/codecov.yml


.PHONY: coverage-libtests coverage-pytests coverage-html clean-coverage

if ENABLE_TEST_COVERAGE
coverage-libtests:
	$(LCOV) --directory tests/libtests --capture --output-file coverage-libtests.info
	$(LCOV) --remove coverage-libtests.info '/usr/*' '/Library/*' "v1" "*/object.h" "*/include/cppunit/*" "*/libtests/*" -o coverage-libtests.info
	$(LCOV) --list coverage-libtests.info

coverage-pytests:
	$(PYTHON_COVERAGE) combine tests/pytests/.coverage
	$(PYTHON_COVERAGE) xml -o coverage-pytests.xml

coverage-html: coverage-libtests coverage-pytests
	genhtml -o coverage-libtests coverage-libtests.info
	$(PYTHON_COVERAGE) html -d coverage-pytests

clean-coverage:
	$(RM) `find . -name "*.gcda"`
	$(RM) `find . -name ".coverage"`

else
coverage-libtests coverage-pytests coverage-html clean-coverage:
	$(warning Test coverage not enabled. Ignoring test coverage targets)
endif


# End of file
