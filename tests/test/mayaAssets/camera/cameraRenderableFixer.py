"""
Validates camera instances.
"""

import maya.cmds

import assetQC.api.register as register
from assetQC.api.fixer import Fixer


class CameraRenderableFixer(Fixer):
    enable = True
    priority = 1
    assetTypes = ['camera']
    hostApps = ['maya']

    def condition(self, ctx):
        return True

    def run(self, context):
        instance = self.getInstance()

        shape = instance.data['shape']
        nodeAttr = shape + '.renderable'
        maya.cmds.setAttr(nodeAttr, 1)

manager = register.getPluginManager()
manager.registerPlugin(CameraRenderableFixer)
