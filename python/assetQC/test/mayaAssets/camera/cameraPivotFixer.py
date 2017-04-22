"""
Validates camera instances.
"""

import assetQC.api.fixer as fixer


class CameraPivotFixer(fixer.Fixer):
    enable = True
    priority = 1
    assetTypes = ['camera']
    hostApps = ['maya']

    def condition(self, ctx):
        return True

    def run(self, context):
        instance = self.getInstance()
        transform = instance.data['transform']

        # Check pivot values are 0.0
        msg = 'Pivot is not valid.'
        attrs = ['rotatePivot', 'rotatePivotTranslate',
                 'scalePivot', 'scalePivotTranslate']
        for attr in attrs:
            for comp in ['X', 'Y', 'Z']:
                firstValue = maya.cmds.setAttr(transform + '.' + attr + comp, 0.0)
                self.assertAlmostEqual(firstValue, 0.0, msg=msg)

        return

