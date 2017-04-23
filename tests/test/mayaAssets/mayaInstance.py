"""
Defines a camera instance of an asset.
"""

import maya.cmds
import assetQC.api.assetInstance as assetInstance


class MayaInstance(assetInstance.AssetInstance):
    def __init__(self, name, assetType=None):
        assert assetType is not None
        super(MayaInstance, self).__init__(name, assetType=assetType)

        # pre-fill with something so the key exists in 'self.data'
        self.setNode(None)

    def getNode(self):
        return self.data['node']

    def setNode(self, value):
        assert isinstance(value, str) or value is None
        if value:
            assert maya.cmds.objExists(value)
        self.data['node'] = value
