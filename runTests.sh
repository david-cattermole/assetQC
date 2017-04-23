#!/bin/sh

#
export ASSETQC_BASE_DIR="${PWD}"
export ASSETQC_CONFIG_PATH="${ASSETQC_BASE_DIR}/tests/test/data/config/config_standard.json"
echo "ASSETQC_BASE_DIR:" ${ASSETQC_BASE_DIR}
echo "ASSETQC_CONFIG_PATH:" ${ASSETQC_CONFIG_PATH}

# run tests
nosetests ./tests/test/runTests.py ./python ./tests/test  \
   --with-coverage --cover-erase --cover-tests --cover-package=assetQC

## run tests with coverage branches (only supported in 'nose 4.x')
#nosetests ./test/runTests.py ./python ./test  \
#   --with-coverage --cover-erase --cover-tests --cover-package=assetQC # --cover-branches
