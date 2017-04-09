"""
Defines a geometry instance of an asset.
"""

import os
import maya.cmds
import assetQC.test.mayaAssets.mayaInstance as mayaInstance


class AnimInstance(mayaInstance.MayaInstance):
    def __init__(self, name):
        super(AnimInstance, self).__init__(name, assetType='anim')

    def getControlNodeList(self):
        return self.data['ctrl_node_list']

    def setControlNodeList(self, values):
        assert isinstance(values, list)
        self.data['ctrl_node_list'] = values

    def getCurveNodeList(self):
        return self.data['curve_node_list']

    def setCurveNodeList(self, values):
        assert isinstance(values, list)
        self.data['curve_node_list'] = values
