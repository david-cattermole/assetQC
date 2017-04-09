"""
Validator object used to validate data.

Given an asset instance validate the asset data.
Multiple validators can be used for each asset type.
Each validator is required to be completely agnostic to other validators.
Validator must not change the scene or must revert the the state before returning.

This is intended to be an object that defines a function which will return
true or false, if the data is valid or not.

"""

import abc
import time
import assetQC.api.baseDataObject as baseDataObject
import assetQC.api.baseTestObject as baseTestObject
import assetQC.api.assetInstance as assetInstance
import assetQC.api.context as context
import assetQC.api.logger as logger


class Validator(baseDataObject.BaseDataObject,
                baseTestObject.BaseTestObject):
    __metaclass__ = abc.ABCMeta

    # static variables
    enable = True
    priority = None
    assetTypes = []
    hostApps = []
    fixers = []

    def __init__(self, instance):
        super(Validator, self).__init__()
        assert isinstance(instance, assetInstance.AssetInstance)
        self.__instance = instance
        self.__status = None
        name = self.getClassName()
        logName = logger.BASE_LOG_NAME + '.' + name
        self.__logger = logger.getLogger(logName)

    def getInstance(self):
        return self.__instance

    @abc.abstractmethod
    def condition(self, ctx):
        """
        Method for base classes to override with a condition that the object
        will run in.
        """
        return True

    def doProcess(self, ctx):
        """
        
        :param ctx: 
        :return: 
        """
        assert isinstance(ctx, context.Context)
        s = time.clock()  # start

        self.preRun(ctx)
        self.run(ctx)
        self.postRun(ctx)

        e = time.clock()  # end
        d = e - s
        self.logDebug('Duration: {0}'.format(d))
        return

    def preRun(self, ctx):
        """
        
        :param ctx: 
        :return: 
        """
        return

    @abc.abstractmethod
    def run(self, ctx):
        """
        
        :param ctx: 
        :return: 
        """
        return

    def postRun(self, ctx):
        """
        
        :param ctx: 
        :return: 
        """
        return

    def logInfo(self, msg):
        return self.__logger.info(msg)

    def logProgress(self, msg, num):
        msg = '{0}% {1}'.format(num, msg)
        return self.__logger.log(logger.LEVEL_PROGRESS, msg)

    def logWarning(self, msg):
        return self.__logger.warning(msg)

    def logFailure(self, msg):
        return self.__logger.log(logger.LEVEL_FAILURE, msg)

    def logError(self, msg):
        return self.__logger.error(msg)

    def logDebug(self, msg):
        return self.__logger.debug(msg)
