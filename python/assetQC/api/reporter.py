"""
Responsible for outputting results of the validator process.

TODO: Work out the best name for this module.
- Reporter
- Outputer
- Harvester
- Feeder
- Printer
- Processor
- ???
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

    def doProcess(self, context):
        assert isinstance(context, assetQC.api.context.Context)
        self.preRun(context)
        self.run(context)
        self.postRun(context)
        return

    def preRun(self, context):
        return

    @abc.abstractmethod
    def run(self, context):
        return

    def postRun(self, context):
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

