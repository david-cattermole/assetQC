"""
Responsible for outputting results of the validator process.
"""

import abc
import assetQC.api.baseDataObject
import assetQC.api.context
import assetQC.api.logger


# TODO: Research the idea of visualising the results of the validation. For
# example, we could any or all of the functions below...
# - Render mayaAssets with a camera
# - generate a email summary
# - trigger export functions
# - assign shaders/colours to mayaAssets that are invalid.
# - do nothing
class Reporter(assetQC.api.baseDataObject.BaseDataObject):
    """
    Reports the context and status of the 'Asset QC' operation.
     
    This class is intended to be sub-classed and extended.
    """

    __metaclass__ = abc.ABCMeta

    # static variables
    enable = True
    priority = None
    assetTypes = []
    hostApps = []

    def __init__(self):
        super(Reporter, self).__init__()

        # name = self.getClassName()
        # _id = self.getObjectHash()
        # self.__logger = assetQC.api.logger.Logger(logName=name, logId=_id)

        name = self.getClassName()
        name = assetQC.api.logger.BASE_LOG_NAME + '.' + name
        self.__logger = assetQC.api.logger.getLogger(name)

    @abc.abstractmethod
    def condition(self, ctx):
        """
        Method for sub-classes to override with a condition that the object
        will run in.

        Return True to indicate the Reporter should be run, False otherwise.
        """
        return True

    def _doProcess(self, ctx):
        """
        High-level function for running the reporter.
        This method is for internal use only.

        :param ctx: Context of function.
        :type ctx: assetQC.api.context.Context
        :return: None
        """
        assert isinstance(ctx, assetQC.api.context.Context)
        self.preRun(ctx)
        self.run(ctx)
        self.postRun(ctx)
        return

    def preRun(self, ctx):
        """
        Run before the Reporter 'run' method. 

        Users can optionally override this method in a sub-class.

        :param ctx: Context of function.
        :type ctx: assetQC.api.context.Context
        :return: None
        """
        return

    @abc.abstractmethod
    def run(self, ctx):
        """
        Runs the reporter function for the Context given. 

        Users MUST override this method in a sub-class.

        :param ctx: Context of function.
        :type ctx: assetQC.api.context.Context 
        :return: None
        """
        return

    def postRun(self, ctx):
        """
        Run after the Reporter 'run' method. 

        Users can optionally override this method in a sub-class.

        :param ctx: Context of function.
        :type ctx: assetQC.api.context.Context 
        :return: None
        """
        return

    def logInfo(self, msg):
        """
        Log an information message against this Reporter object.

        :param msg: Message to log.
        :type msg: str
        :return: None
        """
        return self.__logger.info(msg)

    def logProgress(self, msg, num):
        """
        Log a progress message against this Reporter object.

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
        Log a warning message against this Reporter object.

        :param msg: Message to log.
        :type msg: str
        :return: None
        """
        return self.__logger.warning(msg)

    def logFailure(self, msg):
        """
        Log a failure message against this Reporter object.

        :param msg: Message to log.
        :type msg: str
        :return: None
        """
        return self.__logger.log(logger.LEVEL_FAILURE, msg)

    def logError(self, msg):
        """
        Log an error message against this Reporter object.

        :param msg: Message to log.
        :type msg: str
        :return: None
        """
        return self.__logger.error(msg)

    def logDebug(self, msg):
        """
        Log a debug message against this Reporter object.

        :param msg: Message to log.
        :type msg: str
        :return: None
        """
        return self.__logger.debug(msg)
