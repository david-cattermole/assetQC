"""
Validates camera instances.
"""

import maya.cmds

import assetQC.api.validator
import test.mayaAssets.camera.cameraRenderableFixer as cameraRenderableFixer


class CameraRenderableValidator(assetQC.api.validator.Validator):
    enable = True
    priority = 1
    assetTypes = ['camera']
    hostApps = ['maya']
    fixers = [cameraRenderableFixer.CameraRenderableFixer]

    def condition(self, ctx):
        return True

    def run(self, context):
        instance = self.getInstance()
        shape = instance.data['shape']

        nodeAttr = shape + '.renderable'
        if maya.cmds.getAttr(nodeAttr):
            return

        self.assertTrue(False, msg='Not a renderable camera!')

