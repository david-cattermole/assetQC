"""
Validates camera instances.
"""

import maya.cmds

import assetQC.api.register as register
import assetQC.api.validator as validator
import test.mayaAssets.camera.cameraPivotFixer as cameraPivotFixer


class CameraPivotValidator(validator.Validator):
    enable = True
    priority = 1
    assetTypes = ['camera']
    hostApps = ['maya']
    fixers = [cameraPivotFixer.CameraPivotFixer]

    def condition(self, ctx):
        return True

    def run(self, context):
        assert self.getInstance()
        instance = self.getInstance()
        transform = instance.data['transform']

        # Check pivot values are 0.0
        msg = 'Pivot is not valid.'
        attrs = ['rotatePivot', 'rotatePivotTranslate',
                 'scalePivot', 'scalePivotTranslate']
        for attr in attrs:
            for comp in ['X', 'Y', 'Z']:
                firstValue = maya.cmds.getAttr(transform + '.' + attr + comp)
                self.assertAlmostEqual(firstValue, 0.0, msg=msg)
        return

manager = register.getPluginManager()
manager.registerPlugin(CameraPivotValidator)
