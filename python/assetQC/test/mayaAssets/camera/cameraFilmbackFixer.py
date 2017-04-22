"""
Validates camera instances.
"""

import maya.cmds

import assetQC.api.fixer as fixer


class CameraFilmbackFixer(fixer.Fixer):
    enable = True
    priority = 1
    assetTypes = ['camera']
    hostApps = ['maya']

    def condition(self, ctx):
        return True

    def run(self, context):
        instance = self.getInstance()
        shape = instance.data['shape']

        nodeAttr = shape + '.horizontalFilmAperture'
        maya.cmds.setAttr(nodeAttr, 3.60 / 2.54)  # 36.0mm

        nodeAttr = shape + '.verticalFilmAperture'
        maya.cmds.setAttr(nodeAttr, 2.40 / 2.54)  # 24.0mm
        return

