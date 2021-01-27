#!/bin/bash

# Run tests to generate coverage information. Upload test coverage data.
# Must run codeocov script in top-level source directory.

make -j$(nproc) install
if [ $? != 0 ]; then exit 1; fi


make -j$(nproc) check -C tests/libtests VERBOSE=1
if [ $? != 0 ]; then exit 1; fi

make coverage-libtests
if [ $? != 0 ]; then exit 1; fi

if [ -r coverage-libtests.info ]; then
  pushd ../../src/pythia && \
      bash <(curl -s https://codecov.io/bash) -X gcov -f ../../build/pythia/coverage-libtests.info -F libtests -y ci-config/codecov.yml \
	  || echo "Codecov did not collect coverage reports." && \
      popd
fi

make -j$(nproc) check -C tests/pytests VERBOSE=1
if [ $? != 0 ]; then exit 1; fi

make coverage-pytests
if [ $? != 0 ]; then exit 1; fi

if [ -r coverage-pytests.xml ]; then
  pushd ../../src/pythia && \
      bash <(curl -s https://codecov.io/bash) -X gcov -f ../../build/pythia/coverage-pytests.xml -F pytests -y ci-config/codecov.yml \
	  || echo "Codecov did not collect coverage reports." && \
      popd
fi


exit 0
