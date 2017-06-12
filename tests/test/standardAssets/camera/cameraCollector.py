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
        return True

    def run(self, ctx):
        assert isinstance(ctx, context.Context)
        root = ctx.getRootDirectory()
        assets = stdUtils.listAssets(root)

        for key, item in assets.iteritems():
            if not key:
                continue
            if item['type'] not in self.assetTypes:
                continue
            name = item['name']
            if not ctx.hasInstance(name):
                instance = cameraInstance.CameraInstance(name)
                instance.setFilePath(key)
                ctx.addInstance(instance)
        return True

manager = register.getPluginManager()
manager.registerPlugin(CameraCollector)
