"""
Defines a camera instance of an asset.
"""

import os
import maya.cmds
# from assetQC.api.assetInstance import AssetInstance
import assetQC.test.mayaAssets.mayaInstance as mayaInstance


class TextureInstance(mayaInstance.MayaInstance):
    def __init__(self, name):
        super(TextureInstance, self).__init__(name, assetType='texture')

    # def getNode(self):
    #     return self.data['node']
    #
    # def setNode(self, value):
    #     assert isinstance(value, str)
    #     self.data['node'] = value

    def getAttr(self):
        return self.data['attr']

    def setAttr(self, value):
        assert isinstance(value, str)
        self.data['attr'] = value

    def setNodeAttr(self, value):
        assert isinstance(value, str)
        self.data['nodeAttr'] = value

    def getDirectory(self):
        return self.data['dirPath']

    def setDirectory(self, value):
        assert isinstance(value, str)
        # assert os.path.isdir(value)
        # assert os.path.isabs(value)
        self.data['dirPath'] = value

    def getFilePath(self):
        return self.data['filePath']

    def setFilePath(self, value):
        assert isinstance(value, str)
        # assert os.path.isfile(value)
        # assert os.path.isabs(value)
        self.data['filePath'] = value

    def getFileName(self):
        return self.data['fileName']

    def setFileName(self, value):
        assert isinstance(value, str)
        self.data['fileName'] = value
