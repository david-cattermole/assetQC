"""
Defines a camera instance of an asset.
"""

import test.standardAssets.standardInstance as standardInstance


class CameraInstance(standardInstance.StandardInstance):
    def __init__(self, name):
        super(CameraInstance, self).__init__(name, assetType='camera')

    # def getTransformNode(self):
    #     return self.data['transform']
    #
    # def setTransformNode(self, value):
    #     assert isinstance(value, str)
    #     self.data['transform'] = value
