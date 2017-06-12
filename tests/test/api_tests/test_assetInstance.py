"""
Unit tests for 'assetQC.api.assetInstance'.
"""

import test.baseLib
import assetQC.api.assetInstance
import assetQC.api.validator
import assetQC.api.fixer
import assetQC.api.status


class ExampleValidator(assetQC.api.validator.Validator):
    def condition(self, ctx):
        return True

    def run(self, context):
        return


class ExampleFixer(assetQC.api.fixer.Fixer):
    def condition(self, ctx):
        return True

    def run(self, context):
        return


class TestAssetInstance(test.baseLib.BaseCase):
    def test_create(self):
        cls = assetQC.api.assetInstance.AssetInstance
        x = cls('name')
        self.assertEqual(x.getClassName(), 'AssetInstance')
        self.assertTrue(isinstance(x.getObjectHash(), int))
        self.assertEqual(x.getAssetType(), None)
        self.assertEqual(x.getName(), 'name')
        self.assertTrue(x.isValid())
        self.assertEqual(x.getStatusList(), [])
        self.assertEqual(x.getFixerList(), [])
        self.assertEqual(len(x.getStatusList()), 0)
        self.assertEqual(len(x.getFixerList()), 0)

        x = cls('name', assetType='camera')
        self.assertEqual(x.getAssetType(), 'camera')
        return

    def test_statuses(self):
        cls = assetQC.api.assetInstance.AssetInstance
        statCls = assetQC.api.status.StatusObject
        x = cls('name')
        excp = assetQC.api.status.WarningStatus
        msg = 'The status message.'
        trace = 'The traceback string.'
        validatorObj = None
        fixerObjs = []
        s = statCls(excp, msg, trace, validatorObj, fixerObjs)
        h = s.getHash()

        x.addStatus(s)
        y = x.getStatusList()
        self.assertNotEqual(y, [])
        self.assertEqual(len(y), 1)

        x.removeStatus(h)
        y = x.getStatusList()
        self.assertEqual(y, [])
        self.assertEqual(len(y), 0)

        x.addStatus(s)
        y = x.getStatusList()
        self.assertNotEqual(y, [])
        self.assertEqual(len(y), 1)

        x.clearStatusList()
        y = x.getStatusList()
        self.assertEqual(y, [])
        self.assertEqual(len(y), 0)
        return

    def test_name(self):
        cls = assetQC.api.assetInstance.AssetInstance
        names = ['name', 'the spaces name', '__new-name', 'number.first', 'a']
        for name in names:
            x = cls(name)
            self.assertEqual(name, x.getName())

        self.assertRaises(AssertionError, cls, '')
        return

    def test_fixers(self):
        cls = assetQC.api.assetInstance.AssetInstance
        x = cls('name')
        self.assertEqual(len(x.getFixerList()), 0)
        v = ExampleValidator(x)
        f1 = ExampleFixer(x)
        f2 = ExampleFixer(x)
        x.addFixer(v, f1)
        x.addFixers(v, [f1, f2])
        self.assertEqual(len(x.getFixerList()), 2)
        return

    def test_log(self):
        cls = assetQC.api.assetInstance.AssetInstance
        x = cls('name')
        x.logInfo('Info Message')
        x.logWarning('Warning Message')
        x.logError('Error Message')
        x.logDebug('Debug Message')
        x.logFailure('Failure Message')
        x.logProgress('Progress Message', 50)
        return
