"""
Reports details of the asset QC to the console.
"""
import assetQC.api.baseDataObject as baseDataObject
import assetQC.api.assetInstance as assetInstance
import assetQC.api.reporter as reporter
import assetQC.api.register as register
import assetQC.api.context as context
import assetQC.api.utils as utils


class ConsolePrintReporter(reporter.Reporter):
    enable = True
    priority = 1
    assetTypes = [utils.ASSET_TYPE_ALL]
    hostApps = [utils.HOST_APP_ALL]

    def __init__(self):
        super(self.__class__, self).__init__()
        return

    def condition(self, ctx):
        return True

    def run(self, ctx):
        # passed instances
        lines = utils.formatInstances(ctx, True)
        for line in lines:
            self.logger.info(line)

        # failed instances
        lines = utils.formatInstances(ctx, False)
        for line in lines:
            self.logger.info(line)
        return

manager = register.getPluginManager()
manager.registerPlugin(ConsolePrintReporter)
