"""
Validates geometry instances.
"""

import assetQC.api.register as register
import assetQC.api.validator as validator
import test.standardAssets.geometry.geometryFilmbackFixer as geometryFilmbackFixer


class GeometryShapeValidator(validator.Validator):
    enable = True
    priority = 1
    assetTypes = ['geometry']
    hostApps = ['standalone']
    fixers = []

    def condition(self, ctx):
        return True

    def run(self, context):
        assert self.getInstance()
        instance = self.getInstance()
        self.assertEqual(instance.getAssetType(), 'geometry')

        shapes = instance.getShapes()
        self.assertTrue(len(shapes) > 1)
        return

manager = register.getPluginManager()
manager.registerPlugin(GeometryFilmbackValidator)
