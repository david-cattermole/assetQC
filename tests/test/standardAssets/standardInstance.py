"""
Defines a camera instance of an asset.
"""

import os
import assetQC.api.assetInstance as assetInstance


class StandardInstance(assetInstance.AssetInstance):
    def __init__(self, name, assetType=None):
        assert assetType is not None
        super(StandardInstance, self).__init__(name, assetType=assetType)

        # pre-fill with something so the key exists in 'self.data'
        self.setFilePath(None)

    def getFilePath(self):
        return self.data['filePath']

    def setFilePath(self, value):
        assert isinstance(value, str) or value is None
        if value:
            assert os.path.isfile(value)
        self.data['filePath'] = value
