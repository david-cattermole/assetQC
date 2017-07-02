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
    """
    Defines a validation method 'run' which is used to ensure.
    
    This class is intended to be sub-classed and extended.
    """

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

    @property
    def logger(self):
        return self.__logger

    def getInstance(self):
        return self.__instance

    @abc.abstractmethod
    def condition(self, ctx):
        """
        Method for sub-classes to override with a condition that the object
        will run in.

        Return True to indicate the Validator should be run, False otherwise.
        """
        return True

    def _doProcess(self, ctx):
        """
        High-level function for running the Validator.
        This method is for internal use ONLY.

        :param ctx: Context of function.
        :type ctx: assetQC.api.context.Context
        :return: None
        """
        assert isinstance(ctx, context.Context)
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
        Run before the Validator 'run' method. 

        Users can optionally override this method in a sub-class.

        :param ctx: Context of function.
        :type ctx: assetQC.api.context.Context
        :return: None
        """
        return

    @abc.abstractmethod
    def run(self, ctx):
        """
        Runs the Validator function on the given Asset Instance 

        Users MUST override this method in a sub-class.

        :param ctx: Context of function.
        :type ctx: assetQC.api.context.Context 
        :return: None
        """
        return

    def postRun(self, ctx):
        """
        Run after the Fixer 'run' method. 

        Users can optionally override this method in a sub-class.

        :param ctx: Context of function.
        :type ctx: assetQC.api.context.Context 
        :return: None
        """
        return
