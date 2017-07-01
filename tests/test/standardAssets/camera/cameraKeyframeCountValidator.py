"""
Validates camera instances.
"""

import assetQC.api.register as register
import assetQC.api.validator as validator


class CameraKeyframeCountValidator(validator.Validator):
    enable = True
    priority = 1
    assetTypes = ['camera']
    hostApps = ['standalone']
    fixers = []

    def condition(self, ctx):
        return True

    def run(self, context):
        assert self.getInstance()
        instance = self.getInstance()
        self.assertEqual(instance.getAssetType(), 'camera')

        # # Film Back
        # filmBackWidth = instance.getFilmBackWidth()
        # filmBackHeight = instance.getFilmBackHeight()
        # self.assertAlmostEqual(filmBackWidth, 36.0)
        # self.assertAlmostEqual(filmBackHeight, 24.0)

        # Transforms
        num = 0
        transform = instance.getTransform()
        for attr in transform:
            num += len(attr)
        self.assertNotEqual(num, 0)
        return

manager = register.getPluginManager()
manager.registerPlugin(CameraKeyframeCountValidator)
