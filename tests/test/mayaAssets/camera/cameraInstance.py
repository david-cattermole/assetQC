"""
Defines a camera instance of an asset.
"""

import maya.cmds
import assetQC.api.register as register
import test.mayaAssets.mayaInstance as mayaInstance


class CameraInstance(mayaInstance.MayaInstance):
    def __init__(self, name):
        super(self.__class__, self).__init__(name, assetType='camera')

    def getTransformNode(self):
        return self.data['transform']

    def setTransformNode(self, value):
        assert isinstance(value, str)
        assert maya.cmds.objExists(value)
        self.data['transform'] = value

    def getShapeNode(self):
        return self.data['shape']

    def setShapeNode(self, value):
        assert isinstance(value, str)
        assert maya.cmds.objExists(value)
        self.data['shape'] = value

manager = register.getPluginManager()
manager.registerPlugin(CameraInstance)
