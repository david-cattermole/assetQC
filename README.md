# Asset Quality Check (QC)

Framework designed to collect, validate and report asset data for Animation and Visual Effects applications. The API documentation can be found [here](https://david-cattermole.github.io/assetQC/html/index.html).

This framework is agnostic to software application but was primarily designed with Autodesk Maya in mind. Other software applications may work, but are currently untested.

assetQC is written in Python, supported on Linux and Window, and is easily extensible. The tests contain simple examples for a (non-functioning) computer graphics pipeline.

This Python module is not an end-user tool, but a framework people can use as a basis for data validation.

## Features:

- Asset data validation using custom written tests.
- Automatic finding of assets (collection) using custom written functions.
- Upon invalid data being found, custom functions can be run to attempt an automatic data fix / clean. 
- Reporting framework to return validation details.
- Per-asset exception handling framework
- Example tests for a rudimentary computer graphics pipeline.

## Project Status 

[![Build Status](https://travis-ci.org/david-cattermole/assetQC.svg?branch=master)](https://travis-ci.org/david-cattermole/assetQC)
[![Coverage Status](https://coveralls.io/repos/github/david-cattermole/assetQC/badge.svg?branch=master)](https://coveralls.io/github/david-cattermole/assetQC?branch=master)
[![Code Health](https://landscape.io/github/david-cattermole/assetQC/master/landscape.svg?style=flat)](https://landscape.io/github/david-cattermole/assetQC/master)

## Usage

_To be written._

## Collector

_To be written._

## Validator

_To be written._

## Fixer

_To be written._

## Reporters

_To be written._

## API Documentation

API Documentation can be found [here](https://david-cattermole.github.io/assetQC/html/index.html).

### Running

Set the 'ASSETQC_BASE_DIR' environment variable before running:

`$ env ASSETQC_BASE_DIR='/home/user/maya/2016/scripts/assetQC'`

Or use this in Python code:

`sys.path.append('/home/user/maya/2016/scripts/assetQC')`

See the [./tests/test/](https://github.com/david-cattermole/assetQC/tree/master/tests/test/) directory for a non-production example usage of assetQC; [./tests/test/mayaAssets/](https://github.com/david-cattermole/assetQC/tree/master/tests/test/mayaAssets) contains the maya specific example code.

### Configuration

- `ASSETQC_BASE_DIR`
  - The base directory for the assetQC module.
  - Example; `/home/user/dev/assetQC`
  
- `ASSETQC_LOGGER_CONFIG_PATH`
  - Example; `${ASSETQC_BASE_DIR}/test/`
  
- `ASSETQC_LOGGER_DIR`
  - Example; `${ASSETQC_BASE_DIR}/test/`
  
- `ASSETQC_TEST_BASE_DIR`
  - The base directory for the test functions.
  - Example; `${ASSETQC_BASE_DIR}/test/`
  
- `ASSETQC_TEST_TEMP_DIR`
  - Example; `${ASSETQC_BASE_DIR}/test/tmp/`
  
- `ASSETQC_TEST_DATA_DIR`
  - Example; `${ASSETQC_TEMP_BASE_DIR}/test/data`
  
- `ASSETQC_PLUGIN_SEARCH_PATH`
  - Search in these directories for plugins.
  - Example; `${ASSETQC_TEMP_BASE_DIR}/:${ASSETQC_TEMP_BASE_DIR}/mayaAssets/camera`
  
- `ASSETQC_TEMP_DIR`
  - A temporary directory (used only test)
  - Example; `/tmp/assetQC`

## Install

_To be written._

### Dependencies

- Python 2.6+ (on Windows and Linux)
- Coverage (python package)
- Nose (python package)

### Optional Dependencies

- Autodesk Maya 2016

### Install

_To be written._

# Limitations and Known Bugs

_To be written._
