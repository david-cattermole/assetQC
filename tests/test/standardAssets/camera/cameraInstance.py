"""
Defines a camera instance of an asset.
"""

import assetQC.api.register as register
import test.standardAssets.standardInstance


class CameraInstance(test.standardAssets.standardInstance.StandardInstance):
    def __init__(self, name, fileObj):
        super(self.__class__, self).__init__(name, fileObj, assetType='camera')

    def getTranslateX(self):
        return self.data.get('translateX', [])

    def setTranslateX(self, value):
        assert isinstance(value, float)
        self.data['translateX'] = value

    def getTranslateY(self):
        return self.data.get('translateY', [])

    def setTranslateY(self, value):
        assert isinstance(value, float)
        self.data['translateY'] = value

    def getTranslateZ(self):
        return self.data.get('translateZ', [])

    def setTranslateZ(self, value):
        assert isinstance(value, float)
        self.data['translateZ'] = value

    def getRotateX(self):
        return self.data.get('rotateX', [])

    def setRotateX(self, value):
        assert isinstance(value, float)
        self.data['rotateX'] = value

    def getRotateY(self):
        return self.data.get('rotateY', [])

    def setRotateY(self, value):
        assert isinstance(value, float)
        self.data['rotateY'] = value

    def getRotateZ(self):
        return self.data.get('rotateZ', [])

    def setRotateZ(self, value):
        assert isinstance(value, float)
        self.data['rotateZ'] = value

    def getTransform(self):
        translateX = self.getTranslateX()
        translateY = self.getTranslateY()
        translateZ = self.getTranslateZ()
        rotateX = self.getRotateX()
        rotateY = self.getRotateY()
        rotateZ = self.getRotateZ()
        attrs = [
            translateX, translateY, translateZ,
            rotateX, rotateY, rotateZ
        ]
        return attrs

    def getFilmBackWidth(self):
        return self.data.get('filmBackWidth')

    def setFilmBackWidth(self, value):
        assert isinstance(value, float)
        self.data['filmBackWidth'] = value

    def getFilmBackHeight(self):
        return self.data.get('filmBackHeight')

    def setFilmBackHeight(self, value):
        assert isinstance(value, float)
        self.data['filmBackHeight'] = value

    def getFocalLength(self):
        return self.data.get('focalLength')

    def setFocalLength(self, value):
        assert isinstance(value, float)
        self.data['focalLength'] = value

manager = register.getPluginManager()
manager.registerPlugin(CameraInstance)
