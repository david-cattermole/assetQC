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

Before starting to check assets, you must first define what an asset is and how to test the asset, what to do if it fails, and what data should be printed at the end.

To define the how to check assets, you sub-class from assetQC provided classes and implement some functions.

The assetQC framework contains the following classes for API users:

| Class Type | Description | Sub-Classing Required |
| ---- | ---- | ---- |
| assetQC.api.context.Context | Stores and defines the current environment the tool is running in | No |
| assetQC.api.assetInstance.AssetInstance | May be sub-classed to provide specific asset type properties and convenience functions. | Optional |
| assetQC.api.collector.Collector | Finds assets to be checked | Required |
| assetQC.api.validator.Validator | Performs checks on the given asset | Required |
| assetQC.api.fixer.Fixer | Fixes problems after a Validator fails | Optional |
| assetQC.api.reporter.Reporter | Runs after all validation is performed, used for logging and printing summaries | Optional |

## Collector

Collector classes provide an interface to define how assets are found and the data they contain. The purpose of this class is to add AssetInstance class objects onto the Context class. A single Collector class should be created for each asset type, it is not recommended to create a single Collector to find all assets.

```python
import os
import assetQC.api.assetInstance as assetInstance
import assetQC.api.register as register
import assetQC.api.collector as collector
import assetQC.api.utils as utils


class BasicCollector(collector.Collector):
    enable = True
    priority = 1
    assetTypes = ['basic']
    hostApps = [utils.HOST_APP_STANDALONE]

    def run(self, ctx):
        rootDir = ctx.getRootDirectory()
        fileNames = os.listdir(rootDir)
        for name in fileNames:
            if not ctx.hasInstance(name):
                instance = assetInstance.AssetInstance(name, assetType='basic')
                # This will guarantee the Fixer example is run.
                instance.data['my_custom_field'] = name + '.theAsset'
                ctx.addInstance(instance)
        return True

manager = register.getPluginManager()
manager.registerPlugin(BasicCollector)
```

## Validator

Validator classes define the checks / tests to perform. These are Unit Tests for assets. You may create more than one validator for one asset type. It is recommended to create more classes, each testing a specific aspect of an asset. A Validator may specify a 'Fixer' sub-class to run, in the case that this Validator fails; the use of Fixer classes is optional.  

```python
import assetQC.api.register as register
import assetQC.api.validator as validator
import assetQC.api.utils as utils


class BasicValidator(validator.Validator):
    enable = True
    priority = 1
    assetTypes = ['basic']
    hostApps = [utils.HOST_APP_STANDALONE]
    fixers = [BasicFixer]  # See "Fixer" class example, below.

    def run(self, context):
        instance = self.getInstance()
        name = instance.getName()
        self.assertTrue(name.endswith('.asset'))
        return

manager = register.getPluginManager()
manager.registerPlugin(BasicValidator)

```

## Fixer

Fixer classes are used only in the case a Validator fails and we need to 'fix' the problem. Fixers are defined on the static method variable 'Validator.fixers' (see above).

```python
import assetQC.api.register as register
import assetQC.api.fixer as fixer
import assetQC.api.utils as utils


class BasicFixer(fixer.Fixer):
    enable = True
    priority = 1
    assetTypes = ['basic']
    hostApps = [utils.HOST_APP_STANDALONE]

    def run(self, context):
        instance = self.getInstance()
        field = 'my_custom_field'
        value = instance.data[field]
        # Force the field to conform to the validator.
        value = str(value).rpartition('.')[0]
        value += '.asset'
        instance.data[field] = value
        return True

manager = register.getPluginManager()
manager.registerPlugin(BasicFixer)

```

## Reporters

Reporter classes are run after all checks and fixes have finished. Reporter classes are used to perform an action based on the results of the tests, for example logging, displaying or emailing users the results.

```python
import assetQC.api.reporter as reporter
import assetQC.api.register as register
import assetQC.api.utils as utils


class BasicReporter(reporter.Reporter):
    enable = True
    priority = 1
    assetTypes = [utils.ASSET_TYPE_ALL]
    hostApps = [utils.HOST_APP_ALL]

    def __init__(self):
        super(self.__class__, self).__init__()
        return

    def run(self, ctx):
        # passed instances
        lines = utils.formatInstances(ctx, True)
        for line in lines:
            self.logInfo(line)

        # failed instances
        lines = utils.formatInstances(ctx, False)
        for line in lines:
            self.logInfo(line)
        return

manager = register.getPluginManager()
manager.registerPlugin(BasicReporter)
```

## API Documentation

API Documentation can be found [here](https://david-cattermole.github.io/assetQC/html/index.html).

### Running

Set the 'ASSETQC_BASE_DIR' environment variable before running:

`$ env ASSETQC_BASE_DIR='/home/user/maya/2016/scripts/assetQC'`

Or use this in Python code:

`sys.path.append('/home/user/maya/2016/scripts/assetQC')`

See the [./tests/test/](https://github.com/david-cattermole/assetQC/tree/master/tests/test/) directory for a non-production example usage of assetQC; [./tests/test/mayaAssets/](https://github.com/david-cattermole/assetQC/tree/master/tests/test/mayaAssets) contains the maya specific example code.

### Configuration

| Name | Description | Example |
| ---- | ----------- | ------- |
| ASSETQC_BASE_DIR | Base directory for the assetQC module | /home/user/dev/assetQC |
| ASSETQC_PLUGIN_SEARCH_PATH | Search in these directories for plugins | ${ASSETQC_TEMP_BASE_DIR}/: ${ASSETQC_TEMP_BASE_DIR}/mayaAssets/camera |
| ASSETQC_LOGGER_CONFIG_PATH | Path to the logger config | ${ASSETQC_BASE_DIR}/test/ |
| ASSETQC_LOGGER_DIR | Directory where the logger will save it's files | ${ASSETQC_BASE_DIR}/test/ |
| ASSETQC_TEST_BASE_DIR | Base directory for the test functions | ${ASSETQC_BASE_DIR}/test/ |
| ASSETQC_TEST_TEMP_DIR | Temporary test directory | ${ASSETQC_BASE_DIR}/test/tmp/ |
| ASSETQC_TEST_DATA_DIR | Data directory for testing only | ${ASSETQC_TEMP_BASE_DIR}/test/data/ |
| ASSETQC_TEMP_DIR | Temporary directory | ${TEMP}/assetQC |

See example configuration files in [./config](https://github.com/david-cattermole/assetQC/tree/master/config); for example [./config/config_linux.json](https://github.com/david-cattermole/assetQC/tree/master/config/config_linux.json).

## Dependencies

- Python 2.6+ (on Windows and Linux)
- Coverage (python package)
- Nose (python package)

### Optional Dependencies

- Autodesk Maya 2016

