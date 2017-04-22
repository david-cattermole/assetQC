"""
Defines a camera instance of an asset.
"""

import os
import maya.cmds
import assetQC.test.mayaAssets.mayaInstance as mayaInstance


class ShaderInstance(mayaInstance.MayaInstance):
    def __init__(self, name):
        super(ShaderInstance, self).__init__(name, assetType='shader')

    def getAttrValues(self):
        return self.data['attrValues']

    def setAttrValues(self, value):
        assert isinstance(value, dict)
        self.data['attrValues'] = value