"""
Unit tests for 'assetQC.api.assetInstance'.
"""

import assetQC.api.assetInstance
import test.baseLib


class TestAssetInstance(test.baseLib.BaseCase):
    def test_create(self):
        assetQC.api.assetInstance.AssetInstance('name')
        return


