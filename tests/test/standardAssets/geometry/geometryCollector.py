"""
Gathers geometry assets from the current scene.
"""

import test.standardUtils as stdUtils
import test.standardAssets.geometry.geometryInstance as geometryInstance
import assetQC.api.register as register
import assetQC.api.collector as collector
import assetQC.api.context as context


class GeometryCollector(collector.Collector):
    enable = True
    priority = 1
    assetTypes = ['geometry']
    hostApps = ['standalone']

    def condition(self, ctx):
        return True

    def run(self, ctx):
        assert isinstance(ctx, context.Context)
        root = ctx.getRootDirectory()
        assets = stdUtils.getAssets(root)

        for asset in assets:
            assetType = asset.getType()
            if assetType not in self.assetTypes:
                continue
            name = asset.getName()
            if not ctx.hasInstance(name):
                instance = geometryInstance.GeometryInstance(name, asset)
                ctx.addInstance(instance)
        return True

manager = register.getPluginManager()
manager.registerPlugin(GeometryCollector)
