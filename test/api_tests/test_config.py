"""
Unit tests for 'assetQC.api.assetInstance'.
"""

import sys
import test.baseLib
import assetQC.api.assetInstance


class TestAssetInstance(test.baseLib.BaseCase):
    def test_create(self):
        assetQC.api.assetInstance.AssetInstance('name')
        return


