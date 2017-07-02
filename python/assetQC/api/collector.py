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
    """
    Collects and filters data into AssetInstances of different types.
    
    This class is intended to be sub-classed and extended.
    """
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

    @property
    def logger(self):
        return self.__logger

    @abc.abstractmethod
    def condition(self, ctx):
        """
        Method for sub-classes to override with a condition that the object
        will run in.

        Return True to indicate the Collector should be run, False otherwise.
        """
        return True

    def _doProcess(self, ctx):
        """
        High-level function for running the collector.
        This method is for internal use ONLY.

        :param ctx: Context of function.
        :type ctx: assetQC.api.context.Context
        :return: None
        """
        assert isinstance(ctx, assetQC.api.context.Context)
        s = time.clock()  # start

        self.preRun(ctx)
        self.run(ctx)
        self.postRun(ctx)

        e = time.clock()  # end
        d = e - s
        msg = 'Duration: %s' % d
        self.logger.debug(msg)
        return

    def preRun(self, ctx):
        """
        Run before the Collector 'run' method. 

        Users can optionally override this method in a sub-class.

        :param ctx: Context of function.
        :type ctx: assetQC.api.context.Context
        :return: None
        """
        return

    @abc.abstractmethod
    def run(self, ctx):
        """
        Runs the Collector function in the given context. 

        Users MUST override this method in a sub-class.

        :param ctx: Context of function.
        :type ctx: assetQC.api.context.Context 
        :return: None
        """
        return

    def postRun(self, ctx):
        """
        Run after the Collector 'run' method. 

        Users can optionally override this method in a sub-class.

        :param ctx: Context of function.
        :type ctx: assetQC.api.context.Context
        :return: None
        """
        return
