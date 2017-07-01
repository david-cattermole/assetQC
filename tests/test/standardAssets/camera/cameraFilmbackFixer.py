"""
Validates camera instances.
"""

import assetQC.api.register as register
import assetQC.api.fixer as fixer


class CameraFilmbackFixer(fixer.Fixer):
    enable = True
    priority = 1
    assetTypes = ['camera']
    hostApps = ['standalone']

    def condition(self, ctx):
        return True

    def run(self, context):
        instance = self.getInstance()
        instance.setFilmBackWidth(36.0)
        instance.setFilmBackHeight(24.0)
        return

manager = register.getPluginManager()
manager.registerPlugin(CameraFilmbackFixer)
