"""
Responsible for outputting results of the validator process.
"""

import abc
import time
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
        name = self.getClassName()
        name = assetQC.api.logger.BASE_LOG_NAME + '.' + name
        self.__logger = assetQC.api.logger.getLogger(name)

    @property
    def logger(self):
        return self.__logger

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
