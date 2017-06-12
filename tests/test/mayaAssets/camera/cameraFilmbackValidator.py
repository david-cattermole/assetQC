"""
Validates camera instances.
"""

import maya.cmds

import assetQC.api.register as register
import assetQC.api.validator as validator
import test.mayaAssets.camera.cameraFilmbackFixer as cameraFilmbackFixer


class CameraFilmbackValidator(validator.Validator):
    enable = True
    priority = 1
    assetTypes = ['camera']
    hostApps = ['maya']
    fixers = [cameraFilmbackFixer.CameraFilmbackFixer]

    def condition(self, ctx):
        return True

    def run(self, context):
        assert self.getInstance()
        instance = self.getInstance()
        self.assertEqual(instance.getAssetType(), 'camera')

        shape = instance.data.get('shape', None)
        if not shape:
            raise status.InternalErrorStatus

        # Check filmback values are '135' photography filmback, 36.0mm x 24.0mm
        msg = 'Filmback is not valid.'
        firstValue = maya.cmds.getAttr(shape + '.horizontalFilmAperture')
        secondValue = 3.60 / 2.54  # 36.0mm
        self.assertAlmostEqual(firstValue, secondValue, msg=msg)

        firstValue = maya.cmds.getAttr(shape + '.verticalFilmAperture')
        secondValue = 2.40 / 2.54  # 24.0mm
        self.assertAlmostEqual(firstValue, secondValue, msg=msg)
        return

manager = register.getPluginManager()
manager.registerPlugin(CameraFilmbackValidator)
