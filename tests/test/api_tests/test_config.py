"""
Unit tests for 'assetQC.api.assetInstance'.
"""

import test.baseLib
import assetQC.api.config


class TestAssetInstance(test.baseLib.BaseCase):
    def test_read(self):
        x = []
        x.append(assetQC.api.config.getTempDir())
        x.append(assetQC.api.config.getTestBaseDir())
        x.append(assetQC.api.config.getLoggingConfigPath())
        x.append(assetQC.api.config.getBaseDir())
        x.append(assetQC.api.config.getLoggerDir())
        x.append(assetQC.api.config.getPluginSearchPath())
        x.append(assetQC.api.config.getTestDataDir())
        x.append(assetQC.api.config.getTestTempDir())
        for i in x:
            self.assertTrue(i)
            self.assertTrue(isinstance(i, basestring))
        return


