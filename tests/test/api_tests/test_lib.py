"""
Unit tests for 'assetQC.api.lib'.
"""

import os
import test.baseLib
import test.standardUtils as stdUtils
import assetQC.api.lib as lib
import assetQC.api.context as context


class TestLib(test.baseLib.BaseCase):
    def test_run(self):
        print 'Test Name:', self.id()
        root = self.rootPath()
        data = {'someData': 42}
        stdUtils.createGenericAsset(name='myAsset', root=root, data=data)
        ctx = context.Context(root=root)
        lib.run(ctx=ctx)
        return

    def test_runBadPath(self):
        print 'Test Name:', self.id()
        root = os.path.abspath('/')
        ctx = context.Context(root=root)
        if os.name != 'nt':
            self.assertRaises(OSError, lib.run, ctx)
        else:
            self.assertRaises(WindowsError, lib.run, ctx)
        return

    def test_runSimpleAssets(self):
        print 'Test Name:', self.id()
        root = self.rootPath()

        renderCam = stdUtils.createRenderCameraAsset(root=root)
        plateA = stdUtils.createPlateAsset(name='A', root=root)
        trackCamA = stdUtils.createTrackCameraAsset(subName='A', root=root)
        geom = stdUtils.createSphereGeomAsset(root=root)
        
        ctx = context.Context(root=root)
        lib.run(ctx=ctx)
        return    
