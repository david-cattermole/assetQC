"""

"""
import assetQC.api.baseDataObject as baseDataObject
import assetQC.api.assetInstance as assetInstance
import assetQC.api.reporter as reporter
import assetQC.api.context as context
import assetQC.api.utils as utils


class ConsolePrintReporter(reporter.Reporter):

    # static variables
    enable = True
    priority = 1
    assetTypes = []
    hostApps = []

    def __init__(self):
        super(ConsolePrintReporter, self).__init__()
        return

    def condition(self, ctx):
        return True

    def run(self, ctx):
        # passed instances
        lines = utils.formatInstances(ctx, True)
        for line in lines:
            self.logInfo(line)

        # failed instances
        lines = utils.formatInstances(ctx, False)
        for line in lines:
            self.logInfo(line)
        return


