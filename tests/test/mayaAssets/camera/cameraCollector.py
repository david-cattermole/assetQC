"""
Gathers camera assets from the current scene.
"""

import maya.cmds

import assetQC.api.register as register
import assetQC.api.collector as collector
import assetQC.api.context as context
import test.mayaAssets.camera.cameraInstance

INVALID_NODES = [
    '|persp',
    '|persp|perspShape',
    '|front',
    '|front|frontShape',
    '|side',
    '|side|sideShape',
    '|top',
    '|top|topShape',
]


class CameraCollector(collector.Collector):
    enable = True
    priority = 1
    assetTypes = ['camera']
    hostApps = ['maya']

    def condition(self, ctx):
        return super(self.__class__, self).condition(ctx)

    def run(self, ctx):
        assert isinstance(ctx, context.Context)
        super(self.__class__, self).run(ctx)

        nodes = maya.cmds.ls(cameras=True, long=True)
        for node in nodes:
            if node in INVALID_NODES:
                continue
            transform = str(maya.cmds.listRelatives(node, parent=True,
                                                    fullPath=True)[0])
            name = transform.split('|')[-1]
            if not ctx.hasInstance(name):
                instance = test.mayaAssets.camera.cameraInstance.CameraInstance(name)
                instance.setNode(str(node))
                instance.setTransformNode(transform)
                instance.setShapeNode(str(node))
                ctx.addInstance(instance)
        return True

manager = register.getPluginManager()
manager.registerPlugin(CameraCollector)
