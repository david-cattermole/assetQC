"""
Defines a rig instance of an asset.
"""

import maya.cmds

import assetQC.api.register as register
import test.mayaAssets.mayaInstance as mayaInstance


class RigInstance(mayaInstance.MayaInstance):
    def __init__(self, name):
        super(RigInstance, self).__init__(name, assetType='rig')

    def getRigSetNode(self):
        return self.data['rig_set']

    def setRigSetNode(self, value):
        assert maya.cmds.objExists(value)
        self.data['rig_set'] = value

    def getControlsSetNode(self):
        return self.data['ctrl_set']

    def setControlsSetNode(self, value):
        assert maya.cmds.objExists(value)
        self.data['ctrl_set'] = value

    def getGeometrySetNode(self):
        return self.data['ctrl_set']

    def setGeometrySetNode(self, value):
        assert maya.cmds.objExists(value)
        self.data['geom_set'] = value

manager = register.getPluginManager()
manager.registerPlugin(RigInstance)