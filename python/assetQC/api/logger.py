"""
Wrapper functions for printing to a log. The log may be the console, or a
text file, or the screen.

NOTE: Logger does not yet write to a file.
"""

# TODO: Investigate how we can put loggers into 'AssetInstance' objects, to
# collect information per-instance - rather than some global log that all
# methods write into. This technique would allow better capturing of diagnostic
# information and sorting of information.

import logging as std_logging
import logging.config as std_logging_config
import assetQC.api.config as config

BASE_LOG_NAME = 'assetqc'

# Log levels
LEVEL_NOTSET = std_logging.NOTSET  # 0
LEVEL_DEBUG = std_logging.DEBUG  # 10
LEVEL_INFO = std_logging.INFO  # 20
LEVEL_PROGRESS = 25
LEVEL_WARNING = std_logging.WARNING  # 30
LEVEL_FAILURE = 35
LEVEL_ERROR = std_logging.ERROR  # 40
LEVEL_CRITICAL = std_logging.CRITICAL  # 50

# Configure Logger
std_logging.addLevelName(LEVEL_PROGRESS, 'PROGRESS')
std_logging.addLevelName(LEVEL_FAILURE, 'FAILURE')

# logger = std_logging.getLogger(BASE_LOG_NAME)
#
# # create console handler and set level to debug
# ch = std_logging.StreamHandler()
# ch.setLevel(std_logging.DEBUG)
#
# # create formatter
# # fmt = "%(levelname)s : %(name)s : %(asctime)s : %(message)s"
# fmt = "%(levelname)s : %(name)s : %(message)s"
# formatter = std_logging.Formatter(fmt)
# ch.setFormatter(formatter)
#
# # set level
# logger.setLevel(std_logging.DEBUG)
#
# # add ch to logger
# logger.addHandler(ch)


def getLogger(name):
    assert isinstance(name, str)
    logConfigPath = config.getLoggingConfigPath()
    logConfig = std_logging_config.fileConfig(logConfigPath)
    return std_logging.getLogger(BASE_LOG_NAME)


def info(msg, logger=None):
    # if logger:
    #     logger.info(msg)
    # else:
    getLogger(BASE_LOG_NAME).info(msg)


def progress(msg, num, logger=None):
    msg = '{0}% {1}'.format(num, msg)
    # if logger:
    #     logger.log(LEVEL_PROGRESS, msg)
    # else:
    getLogger(BASE_LOG_NAME).log(LEVEL_PROGRESS, msg)


def warning(msg, logger=None):
    # if logger:
    #     logger.warning(msg)
    # else:
    getLogger(BASE_LOG_NAME).warning(msg)


def failure(msg, logger=None):
    # if logger:
    #     logger.log(LEVEL_FAILURE, msg)
    # else:
    getLogger(BASE_LOG_NAME).log(LEVEL_FAILURE, msg)


def error(msg, logger=None):
    # if logger:
    #     logger.error(msg)
    # else:
    getLogger(BASE_LOG_NAME).error(msg)


def debug(msg, logger=None):
    # if logger:
    #     logger.error(msg)
    # else:
    getLogger(BASE_LOG_NAME).debug(msg)

