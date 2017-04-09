"""
Collector

Defines an object of nodes/objects to be tested - a 'collection' object.

- Plugin used to find assets.
- Can find many AssetsInstances.
"""

import abc
import time
import assetQC.api.baseDataObject as baseDataObject
import assetQC.api.baseTestObject as baseTestObject
import assetQC.api.context
import assetQC.api.logger


class Collector(baseDataObject.BaseDataObject,
                baseTestObject.BaseTestObject):
    __metaclass__ = abc.ABCMeta

    # static variables
    enable = True
    priority = None
    assetTypes = []
    hostApps = []

    def __init__(self):
        super(Collector, self).__init__()
        self.__instanceObjects = []
        name = self.getClassName()
        name = assetQC.api.logger.BASE_LOG_NAME + '.' + name
        self.__logger = assetQC.api.logger.getLogger(name)

    @abc.abstractmethod
    def condition(self, ctx):
        """
        Method for base classes to override with a condition that the object
        will run in.
        """
        return True

    def doProcess(self, ctx):
        assert isinstance(ctx, assetQC.api.context.Context)
        s = time.clock()  # start

        self.preRun(ctx)
        self.run(ctx)
        self.postRun(ctx)

        e = time.clock()  # end
        d = e - s
        # name = self.getClassName()
        self.logDebug('Duration: {0}'.format(d))
        return

    def preRun(self, ctx):
        return

    @abc.abstractmethod
    def run(self, ctx):
        return

    def postRun(self, ctx):
        return

    def logInfo(self, msg):
        return self.__logger.info(msg)

    def logProgress(self, msg, num):
        return self.__logger.progress(msg, num)

    def logWarning(self, msg):
        return self.__logger.warning(msg)

    def logFailure(self, msg):
        return self.__logger.failure(msg)

    def logError(self, msg):
        return self.__logger.error(msg)

    def logDebug(self, msg):
        return self.__logger.debug(msg)
