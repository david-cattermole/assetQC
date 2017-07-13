"""

"""
import assetQC.api.register as register
import assetQC.api.reporter as reporter
import assetQC.api.context as context
import assetQC.api.utils as utils


class AssignShadersReporter(reporter.Reporter):
    enable = False
    priority = 3
    assetTypes = [utils.ASSET_TYPE_ALL]
    hostApps = [utils.HOST_APP_MAYA]

    def __init__(self):
        super(self.__class__, self).__init__()
        return

    def run(self, ctx):
        # self.logInfo('Assign Shaders Reporter')
        # for validFilter in [True, False]:
        #     lines = assetQC.api.utils.formatInstances(ctx, validFilter)
        #     for line in lines:
        #         self.logInfo(line)
        return


manager = register.getPluginManager()
manager.registerPlugin(AssignShadersReporter)
