"""
Defines a geometry instance of an asset.
"""

import assetQC.api.register as register
import test.mayaAssets.mayaInstance as mayaInstance


class GeometryInstance(mayaInstance.MayaInstance):
    def __init__(self, name):
        super(GeometryInstance, self).__init__(name, assetType='geometry')

    def getGeometryList(self):
        return self.data['geom_list']

    def setGeometryList(self, values):
        assert isinstance(values, list)
        self.data['geom_list'] = values

manager = register.getPluginManager()
manager.registerPlugin(GeometryInstance)
