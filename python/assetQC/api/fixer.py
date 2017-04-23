"""
Fixer module - automatically fixes validation problems.

Given a Validator has failed, define a function that will try to fix a 
specific Validation failure.
"""

import abc
import time
import assetQC.api.baseDataObject as baseDataObject
import assetQC.api.baseTestObject as baseTestObject
import assetQC.api.assetInstance as assetInstance
import assetQC.api.context as context
import assetQC.api.logger as logger


class Fixer(baseDataObject.BaseDataObject,
            baseTestObject.BaseTestObject):
    """
    Fixer objects are used to fix validation problems.
    
    Fixer objects are linked to a Validation objects and are optionally defined 
    to automatically fix validation.
    """
    __metaclass__ = abc.ABCMeta

    # static variables
    enable = True
    priority = None
    assetTypes = []
    hostApps = []

    def __init__(self, instance):
        super(Fixer, self).__init__()
        assert isinstance(instance, assetInstance.AssetInstance)
        self.__instance = instance

        name = self.getClassName()
        name = logger.BASE_LOG_NAME + '.' + name
        self.__logger = logger.getLogger(name)

    def getInstance(self):
        """
        Return the AssetInstance object this Fixer will operate on. 
        """
        return self.__instance

    @abc.abstractmethod
    def condition(self, ctx):
        """
        Method for sub-classes to override with a condition that the object
        will run in.

        Return True to indicate the Fixer should be run, False otherwise.
        """
        return True

    def _doProcess(self, ctx):
        """
        High-level function for running the Fixer.
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
        self.logDebug('Duration: {0}'.format(d))
        return

    def preRun(self, ctx):
        """
        Run before the Fixer 'run' method. 

        Users can optionally override this method in a sub-class.

        :param ctx: Context of function.
        :type ctx: assetQC.api.context.Context
        :return: None
        """
        return

    @abc.abstractmethod
    def run(self, ctx):
        """
        Runs the fixing function on the AssetInstance. 

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

    def logInfo(self, msg):
        """
        Log an information message against this Fixer object.

        :param msg: Message to log.
        :type msg: str
        :return: None
        """
        return self.__logger.info(msg)

    def logProgress(self, msg, num):
        """
        Log a progress message against this Fixer object.

        :param msg: Message to log.
        :type msg: str
        :param num: Percentage of the progess, between 0 and 100 inclusive.
        :type num: int
        :return: None
        """
        msg = '{0}% {1}'.format(num, msg)
        return self.__logger.log(logger.LEVEL_PROGRESS, msg)

    def logWarning(self, msg):
        """
        Log a warning message against this Fixer object.

        :param msg: Message to log.
        :type msg: str
        :return: None
        """
        return self.__logger.warning(msg)

    def logFailure(self, msg):
        """
        Log a failure message against this Fixer object.

        :param msg: Message to log.
        :type msg: str
        :return: None
        """
        return self.__logger.log(logger.LEVEL_FAILURE, msg)

    def logError(self, msg):
        """
        Log an error message against this Fixer object.

        :param msg: Message to log.
        :type msg: str
        :return: None
        """
        return self.__logger.error(msg)

    def logDebug(self, msg):
        """
        Log a debug message against this Fixer object.

        :param msg: Message to log.
        :type msg: str
        :return: None
        """
        return self.__logger.debug(msg)
