#!/bin/bash

# Run tests to generate coverage information. Upload test coverage data.
# Must run codeocov script in top-level source directory.

./run_tests.py
if [ $? != 0 ]; then exit 1; fi

if [ -x $PYTHON_COVERAGE ]; then
    $PYTHON_COVERAGE xml -o coverage.xml
fi

if [ -r coverage.xml ]; then
    bash <(curl -s https://codecov.io/bash) -X gcov -f coverage.xml -y ci-config/codecov.yml \
	  || echo "Codecov did not collect coverage reports."
fi

exit 0
