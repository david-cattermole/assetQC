"""
Gathers camera assets from the current scene.
"""

import maya.cmds

import assetQC.api.collector as collector
import assetQC.api.context as context
import test.standardAssets.camera.cameraInstance as cameraInstance


class CameraCollector(collector.Collector):
    enable = True
    priority = 1
    assetTypes = ['camera']
    hostApps = ['standard']

    def condition(self, ctx):
        return True

    def run(self, ctx):
        assert isinstance(ctx, context.Context)
        return True
