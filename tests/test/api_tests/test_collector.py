"""
Unit tests for 'assetQC.api.collector'.
"""

import test.baseLib
import assetQC.api.assetInstance
import assetQC.api.collector


class ExampleCollector(assetQC.api.collector.Collector):
    def condition(self, ctx):
        return True

    def run(self, context):
        return


class TestCollector(test.baseLib.BaseCase):
    def test_create(self):
        x = ExampleCollector()
        self.assertEqual(x.getClassName(), 'ExampleCollector')
        self.assertTrue(isinstance(x.getObjectHash(), int))
        return

    def test_log(self):
        x = ExampleCollector()
        x.logInfo('Info Message')
        x.logWarning('Warning Message')
        x.logError('Error Message')
        x.logDebug('Debug Message')
        x.logFailure('Failure Message')
        x.logProgress('Progress Message', 50)
        return
