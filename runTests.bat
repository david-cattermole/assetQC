@ECHO OFF

setlocal
set ASSETQC_BASE_DIR=D:\Dev\assetQC\
set ASSETQC_CONFIG_PATH=%ASSETQC_BASE_DIR%\tests\test\data\config\config_windows.json
REM echo "ASSETQC_BASE_DIR:" ${ASSETQC_BASE_DIR}
REM echo "ASSETQC_CONFIG_PATH:" ${ASSETQC_CONFIG_PATH}


REM run API tests without coverage branches
nosetests.exe ./tests/test/runTests.py ./python ./tests/test --with-coverage --cover-erase --cover-tests --cover-package=assetQC

REM run API tests with coverage branches (only supported in 'nose 4.x')
REM nosetests.exe ./tests/test/runTests.py ./python ./tests/test --with-coverage --cover-erase --cover-tests --cover-package=assetQC --cover-branches

REM pause
