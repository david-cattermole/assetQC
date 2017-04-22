# Asset Quality Check (QC)

Framework designed to collect, validate and report asset data for Animation and Visual Effects applications.

This framework is agnostic to software application but was primarily designed with Autodesk Maya in mind. Other software applications may work, but are currently untested.

assetQC is written in Python and is easily extendable. The tests contain simple examples for a (non-functioning) computer graphics pipeline.

This Python module is not an end-user tool, but a framework people can use as a basis for data validation.

## Features:

- Asset data validation using custom written tests.
- Automatic finding of assets (collection) using custom written functions.
- Upon invalid data being found, custom functions can be run to attempt an automatic data fix / clean. 
- Reporting framework to return validation details.
- Per-asset exception handling framework
- Example tests for a rudimentary computer graphics pipeline.

## Build Status 

[![Build Status](https://travis-ci.org/david-cattermole/assetQC.svg?branch=master)](https://travis-ci.org/david-cattermole/assetQC)

## Documentation

API Documentation can be found [here](https://david-cattermole.github.io/assetQC/).

## Usage

_To be written._

### Running

`
$ env ASSETQC_BASE_DIR='/home/davidc/maya/2016/scripts'
sys.path.append('/home/davidc/maya/2016/scripts')
`

See the [./test/](https://github.com/david-cattermole/assetQC/tree/master/python/assetQC/test) directory for a non-production example usage of assetQC; [./test/mayaAssets/](https://github.com/david-cattermole/assetQC/tree/master/python/assetQC/test/mayaAssets) contains the maya specific example code.

### Configuration

- ASSETQC_BASE_DIR
  - The base directory for the assetQC module.
  - Example; _"/home/davidc/dev/mayaScripts/trunk/assetQC"_
  
- ASSETQC_LOGGER_CONFIG_PATH
  - Example; _"${ASSETQC_BASE_DIR}/test/"_
  
- ASSETQC_LOGGER_DIR
  - Example; _"${ASSETQC_BASE_DIR}/test/"_
  
- ASSETQC_TEST_BASE_DIR
  - The base directory for the test functions.
  - Example; _"${ASSETQC_BASE_DIR}/test/"_
  
- ASSETQC_TEST_TEMP_DIR
  - Example; _"${ASSETQC_BASE_DIR}/test/tmp/"_
  
- ASSETQC_TEST_DATA_DIR
  - Example; _"${ASSETQC_TEMP_BASE_DIR}/test/data"_
  
- ASSETQC_PLUGIN_SEARCH_PATH
  - Search in these directories for plugins.
  - Example; _"${ASSETQC_TEMP_BASE_DIR}/:${ASSETQC_TEMP_BASE_DIR}/mayaAssets/camera"_
  
- ASSETQC_TEMP_DIR
  - A temporary directory (used only test)
  - Example; _"/tmp/assetQC"_

## Install

_To be written._

### Dependencies

- Python 2.7.x

### Optional Dependencies

- Autodesk Maya 2016

### Install

_To be written._

# Limitations and Known Bugs

_To be written._
