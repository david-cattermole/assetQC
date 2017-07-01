"""
Defines a camera instance of an asset.
"""

import os
import assetQC.api.assetInstance as assetInstance
import test.standardUtils as stdUtils


class StandardInstance(assetInstance.AssetInstance):
    def __init__(self, name, fileObj, assetType=None):
        assert isinstance(fileObj, stdUtils.AssetFile)
        if assetType is None:
            assetType = fileObj.getType()
        name = fileObj.getName()
        super(StandardInstance, self).__init__(name, assetType=assetType)

        # Add data
        self.data.update(fileObj.getData())

        # Set path
        path = fileObj.getPath()
        self.setAssetFilePath(path)

    def getAssetFilePath(self):
        return self.data.get('assetFilePath')

    def setAssetFilePath(self, value):
        assert isinstance(value, str) or value is None
        if value:
            assert os.path.isfile(value)
        self.data['assetFilePath'] = value
