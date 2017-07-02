"""
Defines a camera instance of an asset.
"""

import assetQC.api.register as register
import test.mayaAssets.mayaInstance as mayaInstance


class ShaderInstance(mayaInstance.MayaInstance):
    def __init__(self, name):
        super(self.__class__, self).__init__(name, assetType='shader')

    def getAttrValues(self):
        return self.data['attrValues']

    def setAttrValues(self, value):
        assert isinstance(value, dict)
        self.data['attrValues'] = value

manager = register.getPluginManager()
manager.registerPlugin(ShaderInstance)
