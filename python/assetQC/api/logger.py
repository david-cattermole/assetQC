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


class AssetQCLogger(std_logging.Logger):
    """
    Logger class for AssetQC project.
    
    Added a few helper functions for 'progress' and 'failure'.
     
    All the standard logging functions are in the base class, such as:
    - info
    - warning
    - error
    - debug
    """
    def __init__(self, name):
        std_logging.Logger.__init__(self, name)

    def progress(self, msg, num, **kwargs):
        msg = '{0}% {1}'.format(num, msg)
        self.log(LEVEL_PROGRESS, msg, **kwargs)

    def failure(self, msg, **kwargs):
        self.log(LEVEL_FAILURE, msg, **kwargs)


def getLogger(name=BASE_LOG_NAME):
    """
    
    :param name: The logger dot-separated name.
    :type name: str
    :rtype: std_logging.Manager
    :return: Logging object.
    """
    assert isinstance(name, str)
    logConfigPath = config.getLoggingConfigPath()

    # Set the logger class.
    std_logging.setLoggerClass(AssetQCLogger)

    # Configure Logger
    std_logging.addLevelName(LEVEL_PROGRESS, 'PROGRESS')
    std_logging.addLevelName(LEVEL_FAILURE, 'FAILURE')
    std_logging_config.fileConfig(logConfigPath)

    logger = std_logging.getLogger(name)
    assert isinstance(logger, AssetQCLogger)
    return logger
