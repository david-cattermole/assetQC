"""
Defines a imageSequence instance of an asset.
"""

import assetQC.api.register as register
import test.standardAssets.standardInstance as standardInstance


class ImageSequenceInstance(standardInstance.StandardInstance):
    def __init__(self, name, fileObj):
        super(ImageSequenceInstance, self).__init__(name, fileObj, assetType='imageSequence')

    def getImagePath(self):
        return self.data.get('path')

    def setImagePath(self, value):
        assert isinstance(value, basestring)
        self.data['path'] = value

    def getFileName(self):
        return self.data.get('path')

    def setFileName(self, value):
        assert isinstance(value, basestring)
        self.data['path'] = value

    def getDirPath(self):
        return self.data.get('path')

    def setDirPath(self, value):
        assert isinstance(value, basestring)
        self.data['path'] = value 

manager = register.getPluginManager()
manager.registerPlugin(ImageSequenceInstance)
