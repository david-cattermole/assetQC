"""
Gathers camera assets from the current scene.
"""

import test.standardUtils as stdUtils
import test.standardAssets.camera.cameraInstance as cameraInstance
import assetQC.api.register as register
import assetQC.api.collector as collector
import assetQC.api.context as context


class CameraCollector(collector.Collector):
    enable = True
    priority = 1
    assetTypes = ['camera']
    hostApps = ['standalone']

    def condition(self, ctx):
        return super(self.__class__, self).condition(ctx)

    def run(self, ctx):
        assert isinstance(ctx, context.Context)
        super(self.__class__, self).run(ctx)

        root = ctx.getRootDirectory()
        assets = stdUtils.getAssets(root)

        for asset in assets:
            assetType = asset.getType()
            if assetType not in self.assetTypes:
                continue
            name = asset.getName()
            if not ctx.hasInstance(name):
                instance = cameraInstance.CameraInstance(name, asset)
                ctx.addInstance(instance)
        return True

manager = register.getPluginManager()
manager.registerPlugin(CameraCollector)
