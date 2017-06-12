"""
Validates camera instances.
"""

import assetQC.api.register as register
import assetQC.api.validator as validator
import test.standardAssets.camera.cameraFilmbackFixer as cameraFilmbackFixer


class CameraFilmbackValidator(validator.Validator):
    enable = True
    priority = 1
    assetTypes = ['camera']
    hostApps = ['standalone']
    fixers = [cameraFilmbackFixer.CameraFilmbackFixer]

    def condition(self, ctx):
        return True

    def run(self, context):
        assert self.getInstance()
        instance = self.getInstance()
        self.assertEqual(instance.getAssetType(), 'camera')
        return


manager = register.getPluginManager()
manager.registerPlugin(CameraFilmbackValidator)