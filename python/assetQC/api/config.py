"""
Module for reading data from the config (or overridden with environment variables)
"""

import os
import re
import json
import collections
import functools

CONFIG_ENTRY_NAMES = [
    'ASSETQC_BASE_DIR',
    'ASSETQC_TEMP_DIR',
    'ASSETQC_TEST_BASE_DIR',
    'ASSETQC_TEST_TEMP_DIR',
    'ASSETQC_TEST_DATA_DIR',
    'ASSETQC_LOGGER_CONFIG_PATH',
    'ASSETQC_LOGGER_DIR',
    'ASSETQC_PLUGIN_SEARCH_PATH',
]


class memoized(object):
    """
    Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    
    From:
    https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
    """

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        if not isinstance(args, collections.Hashable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return self.func(*args)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value

    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__

    def __get__(self, obj, objtype):
        """Support instance methods."""
        return functools.partial(self.__call__, obj)


@memoized
def __readData(filePath):
    """
    Read file path as JSON data format.
    
    :param filePath: File path to .json file. 
    :return: Contents of the .json file.
    """
    f = open(filePath, 'rb')
    data = json.load(f)
    f.close()
    return data


def __readConfig():
    """
    Get the configuration file contents.
    """
    configPath = os.getenv('ASSETQC_CONFIG_PATH', None)
    data = {}
    if configPath and os.path.isfile(configPath):
        data = __readData(configPath)
    else:
        raise ValueError('Configuration file cannot be found.')
    return data


def __getValue(key, expand=True):
    """
    Get the value from the environment or config file.
    
    :param key: 
    :return: 
    """
    assert isinstance(key, (str, unicode))

    # look at the environment first, if it does not exist fallback to the
    # config file.
    result = None
    if key in os.environ:
        result = os.environ[key]
    else:
        data = __readConfig()
        if data and key in data:
            result = data[key]

    if result and expand == True:
        result = __expandTokens(result)

    return result


def __expandValue(value):
    result = value
    for name in CONFIG_ENTRY_NAMES:
        key = '${' + name + '}'
        if key in result:
            keyValue = __getValue(name, expand=False)
            result = result.replace(key, keyValue)
    return result


def __expandTokens(value):
    result = None
    if isinstance(value, (str, unicode)):
        result = __expandValue(value)
    elif isinstance(value, list):
        result = []
        for v in value:
            v = __expandValue(v)
            result.append(v)
    return result


def getLoggingConfigPath():
    """

    :return: 
    """
    result = __getValue('ASSETQC_LOGGER_CONFIG_PATH')
    assert isinstance(result, (str, unicode))
    return result


def getBaseDir():
    """
    
    :return: 
    """
    result = __getValue('ASSETQC_BASE_DIR')
    assert isinstance(result, (str, unicode))
    return result


def getTempDir():
    """

    :return: 
    """
    result = __getValue('ASSETQC_TEMP_DIR')
    assert isinstance(result, (str, unicode))
    return result


def getTestBaseDir():
    """

    :return: 
    """
    result = __getValue('ASSETQC_TEST_BASE_DIR')
    assert isinstance(result, (str, unicode))
    return result


def getTestTempDir():
    """

    :return: 
    """
    result = __getValue('ASSETQC_TEST_TEMP_DIR')
    assert isinstance(result, (str, unicode))
    return result


def getTestDataDir():
    """

    :return: 
    """
    result = __getValue('ASSETQC_TEST_DATA_DIR')
    assert isinstance(result, (str, unicode))
    return result


def getLoggerDir():
    """
    
    :return: 
    """
    result = __getValue('ASSETQC_LOGGER_DIR')
    assert isinstance(result, (str, unicode))
    return result


def getPluginSearchPath():
    """
    
    :return: 
    """
    result = ''
    value = __getValue('ASSETQC_PLUGIN_SEARCH_PATH')
    assert isinstance(value, list) or isinstance(value, (str, unicode))
    if isinstance(value, list):
        for v in value:
            result += v
    elif isinstance(value, (str, unicode)):
        result = value
    return result
