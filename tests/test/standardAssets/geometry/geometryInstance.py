"""
Defines a geometry instance of an asset.
"""

import assetQC.api.register as register
import test.standardAssets.standardInstance as standardInstance


class GeometryInstance(standardInstance.StandardInstance):
    def __init__(self, name, fileObj):
        super(GeometryInstance, self).__init__(name, fileObj, assetType='geometry')

    def getShapes(self):
        return self.data.get('shapes')

    def setShapes(self, value):
        assert isinstance(value, list)
        self.data['shapes'] = value

    def getFaceNum(self):
        return self.data.get('faceNum')

    def setFaceNum(self, value):
        assert isinstance(value, list)
        self.data['faceNum'] = value

    def getVertNum(self):
        return self.data.get('vertNum')

    def setVertNum(self, value):
        assert isinstance(value, list)
        self.data['vertNum'] = value


manager = register.getPluginManager()
manager.registerPlugin(GeometryInstance)
