"""
Unit tests for 'assetQC.api.context'.
"""

import os.path
import test.baseLib
import assetQC.api.context
import assetQC.api.assetInstance
import assetQC.api.config
import assetQC.api.register
import assetQC.api.utils

# class ExampleInstance(assetQC.api.assetInstance.AssetInstance):
#     pass



class TestContext(test.baseLib.BaseCase):
    def test_create(self):
        cls = assetQC.api.context.Context
        x = cls()
        self.assertEqual(x.getClassName(), 'Context')

        mgr = assetQC.api.register.PluginManager()
        root = assetQC.api.config.getBaseDir()
        host = assetQC.api.utils.HOST_APP_STANDALONE
        cls(pluginManager=None, root=None, hostApp=host)
        cls(pluginManager=None, root=root, hostApp=None)
        cls(pluginManager=mgr, root=None, hostApp=None)

        z = cls(pluginManager=mgr, root=root, hostApp=host)
        self.assertEqual(z.getClassName(), 'Context')
        self.assertTrue(isinstance(z.getObjectHash(), int))
        self.assertTrue(mgr is z.getPluginManager())
        self.assertTrue(z.getEnvVar('PATH'))
        self.assertEqual(z.getHostApp(), host)
        self.assertTrue(isinstance(z.getHostApp(), str))
        self.assertTrue(isinstance(z.getHostName(), str))
        self.assertEqual(z.getRootDirectory(), root)
        self.assertTrue(isinstance(z.getRootDirectory(), str))
        self.assertTrue(isinstance(z.getUserEmailAddress(), str))
        self.assertTrue(isinstance(z.getUserName(), str))

    def test_instances(self):
        cls = assetQC.api.context.Context
        instCls = assetQC.api.assetInstance.AssetInstance
        # instCls = ExampleInstance

        root = assetQC.api.config.getBaseDir()
        x = cls()
        instances = []
        for i in xrange(10):
            name = 'name' + str(i)
            instance = instCls(name, assetType='asset')
            instance.data['myCustomData'] = os.path.join(root, name)
            instances.append(instance)
        x.addInstances(instances)
        x.getInstances(sortByName=True)
        x.getInstances(sortByDataKeyword=True, dataKeyword='myCustomData')
        for i in xrange(10):
            name = 'name' + str(i)
            x.hasInstance(name)
        x.clearInstances()




