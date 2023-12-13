#!/bin/bash
#
# WARNING: If test coverage is enabled, this script downlaods the
# CodeCov uploader for Linux.
#
# Run tests to generate coverage information. Upload test coverage data.
# Must run codeocov script in top-level source directory.

SRC_DIR=`pwd`
BUILD_DIR=${SRC_DIR}/../../build/pythia

cd ${BUILD_DIR}

make -j$(nproc) check -C tests/libtests VERBOSE=1
if [ $? != 0 ]; then exit 1; fi

make coverage-libtests
if [ $? != 0 ]; then exit 1; fi

if [ -r coverage-libtests.info ]; then
    curl https://keybase.io/codecovsecurity/pgp_keys.asc | gpg --no-default-keyring --keyring trustedkeys.gpg --import
    curl -Os https://uploader.codecov.io/latest/linux/codecov
    curl -Os https://uploader.codecov.io/latest/linux/codecov.SHA256SUM
    curl -Os https://uploader.codecov.io/latest/linux/codecov.SHA256SUM.sig
    gpgv codecov.SHA256SUM.sig codecov.SHA256SUM
    if [ $? != 0 ]; then exit 1; fi
    shasum -a 256 -c codecov.SHA256SUM
    if [ $? != 0 ]; then exit 1; fi
    chmod +x codecov

    pushd ${SRC_DIR} && \
      ${BUILD_DIR}/codecov -C ${BUILD_SOURCEVERSION} -r geodynamics/pythia -f ${BUILD_DIR}/coverage-libtests.info -F libtests -y ci-config/codecov.yml \
	  || echo "Codecov did not collect coverage reports." && \
      popd
fi

make -j$(nproc) check -C tests/pytests VERBOSE=1
if [ $? != 0 ]; then exit 1; fi

make coverage-pytests
if [ $? != 0 ]; then exit 1; fi

if [ -r coverage-pytests.xml ]; then
  pushd ${SRC_DIR} && \
      ${BUILD_DIR}/codecov -C ${BUILD_SOURCEVERSION} -r geodynamics/pythia -f ${BUILD_DIR}/coverage-pytests.xml -F pytests -y ci-config/codecov.yml \
	  || echo "Codecov did not collect coverage reports." && \
      popd
fi


exit 0
