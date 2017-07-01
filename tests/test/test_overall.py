"""
Test the entire package, overall.
"""

import os
import sys

import test.baseLib
import test.standardUtils as stdUtils
import assetQC.api.lib as lib
import assetQC.api.context as context
import assetQC.api.register as register
import assetQC.api.config as config


class TestOverall(test.baseLib.BaseCase):
    def test_simpleAssets(self):
        print 'Test Name:', self.id()
        root = self.rootPath()
        
        renderCam = stdUtils.createRenderCameraAsset(root=root)

        plateA = stdUtils.createPlateAsset(name='A', root=root)
        plateB = stdUtils.createPlateAsset(name='B', root=root)

        trackCamA = stdUtils.createTrackCameraAsset(subName='A', root=root)
        trackCamB = stdUtils.createTrackCameraAsset(subName='B', root=root)

        geom = stdUtils.createSphereGeomAsset(root=root)

        # rig = stdUtils.createCharacterRigAsset(name='adam', root=root)

        metalShd = stdUtils.createMetalShaderAsset(root=root)
        woodShd = stdUtils.createWoodShaderAsset(root=root)

        # do checks
        ctx = context.Context(root=root)
        lib.run(ctx=ctx)
        return

    def test_cameraValidator(self):
        print 'Test Name:', self.id()
        root = self.rootPath()

        name = 'camera'
        data = {
            'focalLength': 50.0,
            'filmBackWidth': 42.0,
            'filmBackHeight': 42.0
        }
        cam = stdUtils.createCameraAsset(root=root, name=name, data=data)

        ctx = context.Context(root=root)
        lib.run(ctx=ctx)
        return

    def test_geometryValidator(self):
        print 'Test Name:', self.id()
        root = self.rootPath()

        name = 'geom'
        data = {
            'shapes': [],
            'faceNum': -1,
            'vertNum': -1
        }
        cam = stdUtils.createGeometryAsset(root=root, name=name, data=data)

        ctx = context.Context(root=root)
        lib.run(ctx=ctx)
        return
    
    def test_three(self):
        print 'Test Name:', self.id()
        root = self.rootPath()
        
        renderCam = stdUtils.createRenderCameraAsset(root=root)

        plateA = stdUtils.createPlateAsset(name='A', root=root)
        plateB = stdUtils.createPlateAsset(name='B', root=root)

        trackCamA = stdUtils.createTrackCameraAsset(subName='A', root=root)
        trackCamB = stdUtils.createTrackCameraAsset(subName='B', root=root)

        geom = stdUtils.createSphereGeomAsset(root=root)

        metalShd = stdUtils.createMetalShaderAsset(root=root)
        woodShd = stdUtils.createWoodShaderAsset(root=root)

        # do checks
        ctx = context.Context(root=root)
        lib.run(ctx=ctx)
        return
