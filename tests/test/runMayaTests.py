"""
Runs tests for the 'check assets' API.

Run this file with this shell command:
$ env ASSETQC_CONFIG_PATH='/home/davidc/dev/mayaScripts/trunk/assetQC/test/config/config.json' mayapy runTests.py
"""

import os
try:
    import maya.standalone
    maya.standalone.initialize()
except:
    pass
import maya.cmds

# # for testing, make sure the Maya scripts are in the 'PYTHONPATH'.
# # TODO: Replace with config entry 'ASSETQC_TEST_BASE_DIR'.
# sys.path.append('/home/davidc/maya/2016/scripts')


# configDir = '/home/davidc/dev/mayaScripts/trunk/assetQC/test/config/config.json'
# # os.putenv('ASSETQC_CONFIG_PATH', configDir)
# os.environ['ASSETQC_CONFIG_PATH'] = configDir

import assetQC.api.config as config
import assetQC.api.lib as lib
import assetQC.api.context as context
import test.mayaAssets.camera.cameraCollector as cameraCollector
import test.mayaAssets.camera.cameraRenderableValidator as cameraRenderableValidator
import test.mayaAssets.camera.cameraKeyframeCountValidator as cameraKeyframeCountValidator
import test.mayaAssets.camera.cameraFilmbackValidator as cameraFilmbackValidator
import test.mayaAssets.rig.rigCollector as rigCollector
import test.mayaAssets.rig.rigValidator as rigValidator
import test.mayaUtils as mayaUtils


def test1():
    print ''
    print 'TEST 1 ' + ('=' * 80)

    # time
    start = 1001
    end = 1010
    middle = start + ((end - start) * 0.5)

    # New scene
    mayaUtils.reinitializeScene(frameRange=(start, end))

    # create camera
    tfm, shp = mayaUtils.createCameraAsset('renderCamera')
    maya.cmds.setAttr(shp + '.renderable', 1)
    maya.cmds.setKeyframe(tfm, at='translateX', t=start, v=0.0)
    maya.cmds.setKeyframe(tfm, at='translateY', t=end, v=5.0)
    maya.cmds.setKeyframe(tfm, at='translateZ', t=middle, v=-10.0)
    mayaUtils.saveTestFile('test1_before')

    # do checks
    ctx = context.Context(find=context.FIND_MODE_ALL)
    lib.run(ctx=ctx)

    # save the scene
    mayaUtils.saveTestFile('test1_after')
    return


def test2():
    print ''
    print 'TEST 2 ' + ('=' * 80)

    # New Scene
    start = 1001
    end = 1010
    mayaUtils.reinitializeScene(frameRange=(start, end))

    # create cameras
    tfm1, shp1 = mayaUtils.createCameraAsset('camera1')
    tfm2, shp2 = mayaUtils.createCameraAsset('camera2')
    tfm3, shp3 = mayaUtils.createCameraAsset('camera3')
    tfm4, shp4 = mayaUtils.createCameraAsset('camera4')
    maya.cmds.setAttr(shp1 + '.renderable', 1)
    maya.cmds.setAttr(shp2 + '.renderable', 1)
    maya.cmds.setAttr(shp3 + '.renderable', 0)
    maya.cmds.setAttr(shp4 + '.renderable', 1)
    maya.cmds.setAttr(shp4 + '.horizontalFilmAperture', 1.0)
    maya.cmds.setAttr(shp4 + '.verticalFilmAperture', 1.0)
    maya.cmds.setAttr('persp.renderable', 0)
    maya.cmds.setKeyframe(tfm1, at='rotateX', t=start, v=0.0)
    maya.cmds.setKeyframe(tfm1, at='rotateY', t=start, v=-0.0)
    maya.cmds.setKeyframe(tfm1, at='rotateZ', t=start, v=-0.0)

    # create sphere rig
    sphere = maya.cmds.polySphere()[0]
    ctrl = maya.cmds.circle(nr=(0, 1, 0), radius=2)[0]
    mayaUtils.createRigAsset(name='characterSphereName',
                             geomList=[sphere], ctrlList=[ctrl])

    # create cube rig
    cube = maya.cmds.polyCube()[0]
    ctrl = maya.cmds.circle(nr=(0, 1, 0), radius=2)[0]
    mayaUtils.createRigAsset(name='characterCubeName',
                             geomList=[cube], ctrlList=[ctrl])

    # save scene before test
    mayaUtils.saveTestFile('test2_before')

    # check context
    ctx = context.Context(find=context.FIND_MODE_NONE)

    # camera
    ctx.addCollectorPlugin(cameraCollector.CameraCollector)
    ctx.addValidatorPlugin(cameraRenderableValidator.CameraRenderableValidator)
    ctx.addValidatorPlugin(
        cameraKeyframeCountValidator.CameraKeyframeCountValidator)
    ctx.addValidatorPlugin(cameraFilmbackValidator.CameraFilmbackValidator)

    # rig
    ctx.addCollectorPlugin(rigCollector.RigCollector)
    ctx.addValidatorPlugin(rigValidator.RigValidator)

    # standardReporters
    ctx.findReporterPlugins()

    # run check
    lib.run(ctx=ctx)

    # save the scene
    mayaUtils.saveTestFile('test2_after')
    return


def test3():
    print ''
    print 'TEST 3 ' + ('=' * 80)

    # New Scene
    start = 1001
    end = 1010
    mayaUtils.reinitializeScene(frameRange=(start, end))

    # create camera
    tfm, shp = mayaUtils.createCameraAsset('renderCamera')
    maya.cmds.setAttr(shp + '.renderable', 1)
    maya.cmds.setKeyframe(tfm, at='rotateX', t=start, v=0.0)
    maya.cmds.setKeyframe(tfm, at='rotateY', t=start, v=-0.0)
    maya.cmds.setKeyframe(tfm, at='rotateZ', t=start, v=-0.0)

    # create cube rig
    cube = maya.cmds.polyCube()[0]
    ctrl = maya.cmds.circle(nr=(0, 1, 0), radius=2)[0]
    mayaUtils.createRigAsset(name='characterCubeName',
                             geomList=[cube], ctrlList=[ctrl])
    maya.cmds.setKeyframe(ctrl, at='translateX', t=start, v=1.0)
    maya.cmds.setKeyframe(ctrl, at='translateY', t=start, v=-3.0)
    maya.cmds.setKeyframe(ctrl, at='translateZ', t=start, v=-4.0)
    maya.cmds.setKeyframe(ctrl, at='translateX', t=end, v=-1.0)
    maya.cmds.setKeyframe(ctrl, at='translateY', t=end, v=3.0)
    maya.cmds.setKeyframe(ctrl, at='translateZ', t=end, v=4.0)

    # save file
    mayaUtils.saveTestFile('test3_before')

    # do checks
    ctx = context.Context(find=context.FIND_MODE_NONE)
    ctx.findCollectorPlugins()
    ctx.findValidatorPlugins()
    ctx.findReporterPlugins()
    lib.run(ctx=ctx)

    # save the scene
    mayaUtils.saveTestFile('test3_after')
    return


def test4():
    print ''
    print 'TEST 4 ' + ('=' * 80)

    # New Scene
    start = 1001
    end = 1010
    mayaUtils.reinitializeScene(frameRange=(start, end))

    # create shaders
    mayaUtils.createShaderAsset('redPaint',
                                nodeType='blinn',
                                color=(0.7, 0.2, 0.2))
    mayaUtils.createShaderAsset('bluePaint',
                                nodeType='blinn',
                                color=(0.2, 0.2, 0.7))
    mayaUtils.createShaderAsset('grey',
                                nodeType='lambert',
                                color=(0.5, 0.5, 0.5))
    mayaUtils.createShaderAsset('glass',
                                nodeType='phong',
                                color=(1.0, 1.0, 1.0))
    mayaUtils.saveTestFile('test4_before')

    # do checks
    lib.run()

    # save the scene
    mayaUtils.saveTestFile('test4_after')
    return


def test5():
    print ''
    print 'TEST 5 ' + ('=' * 80)
    testBaseDir = config.getTestBaseDir()

    # New Scene
    start = 1001
    end = 1010
    mayaUtils.reinitializeScene(frameRange=(start, end))

    # create shaders
    uvShd, uvShdGrp = mayaUtils.createShaderAsset('uvTest', nodeType='lambert',
                                                  color=(0.5, 0.5, 0.5))
    woodShd, woodShdGrp = mayaUtils.createShaderAsset('wood', nodeType='blinn',
                                                      color=(0.5, 0.5, 0.5))

    # create uv shader textures
    testUvs = os.path.join(testBaseDir, 'uvTestTexture.jpg')
    uvTx = mayaUtils.createTextureAsset('uvTestTexture', nodeType='file', path=testUvs)
    mayaUtils.connectTextureToShader(uvTx, uvShd, 'color')

    # create wood shader textures
    woodColorPath = os.path.join(testBaseDir, 'WD025/WD025_Square.jpg')
    woodSpecPath = os.path.join(testBaseDir, 'WD025/WD025_Square_Spec.jpg')
    woodNormPath = os.path.join(testBaseDir, 'WD025/WD025_Square_NORM.jpg')
    woodBumpPath = os.path.join(testBaseDir, 'WD025/WD025_Square_Bump.jpg')
    woodColorTx = mayaUtils.createTextureAsset('woodColor', nodeType='file', path=woodColorPath)
    woodSpecTx = mayaUtils.createTextureAsset('woodSpec', nodeType='file', path=woodSpecPath)
    woodNormTx = mayaUtils.createTextureAsset('woodNorm', nodeType='file', path=woodNormPath)
    woodBumpTx = mayaUtils.createTextureAsset('woodBump', nodeType='file', path=woodBumpPath)
    mayaUtils.connectTextureToShader(woodColorTx, woodShd, 'color')
    mayaUtils.connectTextureToShader(woodSpecTx, woodShd, 'specularColor')
    mayaUtils.saveTestFile('test5_before')

    # do checks
    lib.run()

    # save the scene
    mayaUtils.saveTestFile('test5_after')
    return


def test6():
    print ''
    print 'TEST 6 ' + ('=' * 80)
    testBaseDir = config.getTestBaseDir()

    # New Scene
    start = 1001
    end = 1010
    mayaUtils.reinitializeScene(frameRange=(start, end))

    # create camera
    tfm, shp = mayaUtils.createCameraAsset('renderCamera')
    maya.cmds.setAttr(shp + '.renderable', 1)
    maya.cmds.setKeyframe(tfm, at='translateZ', t=start, v=4.0)
    maya.cmds.setKeyframe(tfm, at='translateZ', t=end, v=6.0)
    maya.cmds.setKeyframe(tfm, at='rotateX', t=start, v=0.0)
    maya.cmds.setKeyframe(tfm, at='rotateX', t=end, v=-5.0)

    # create cube rig
    cube = maya.cmds.polyCube()[0]
    ctrl = maya.cmds.circle(nr=(0, 1, 0), radius=2)[0]
    mayaUtils.createRigAsset(name='characterCubeName',
                             geomList=[cube], ctrlList=[ctrl])
    maya.cmds.setKeyframe(ctrl, at='translateX', t=start, v=-1.0)
    maya.cmds.setKeyframe(ctrl, at='translateX', t=end, v=1.0)
    maya.cmds.setKeyframe(ctrl, at='rotateY', t=start, v=-45.0)
    maya.cmds.setKeyframe(ctrl, at='rotateY', t=end, v=45.0)

    # create shaders
    uvShd, uvShdGrp = mayaUtils.createShaderAsset('uvTest', nodeType='lambert',
                                                  color=(0.5, 0.5, 0.5))
    # mayaUtils.assignShaderAsset([cube], uvShdGrp)
    mayaUtils.assignObjectListToShader(objList=[cube], shader=uvShd)

    # create uv shader textures
    testUvs = os.path.join(testBaseDir, 'uvTestTexture.jpg')
    uvTx = mayaUtils.createTextureAsset('uvTestTexture', path=testUvs)
    mayaUtils.connectTextureToShader(uvTx, uvShd, 'color')

    # save scene before test
    mayaUtils.saveTestFile('test6_before')

    # do checks
    lib.run()

    # save the scene
    mayaUtils.saveTestFile('test6_after')
    return


def test7():
    print ''
    print 'TEST 7 ' + ('=' * 80)

    # new scene
    start = 1001
    end = 1010
    mayaUtils.reinitializeScene(frameRange=(start, end))

    # create geometry
    sphere = maya.cmds.polySphere()[0]
    geomList = [sphere]
    geomSet = mayaUtils.createGeometryAsset(name='sphereGeom',
                                            geomList=geomList)
    mayaUtils.saveTestFile('test7_before')

    # do checks
    ctx = context.Context(find=context.FIND_MODE_ALL)
    lib.run(ctx=ctx)

    # save the scene
    mayaUtils.saveTestFile('test7_after')
    return


def test8():
    print ''
    print 'TEST 8 ' + ('=' * 80)
    testBaseDir = config.getTestBaseDir()

    # New Scene
    start = 1001
    end = 1010
    mayaUtils.reinitializeScene(frameRange=(start, end))

    # create camera
    for i in xrange(100):
        tfm, shp = mayaUtils.createCameraAsset('renderCamera1')
        maya.cmds.setAttr(shp + '.renderable', 1)
        maya.cmds.setKeyframe(tfm, at='translateZ', t=start, v=4.0)
        maya.cmds.setKeyframe(tfm, at='translateZ', t=end, v=6.0)
        maya.cmds.setKeyframe(tfm, at='rotateX', t=start, v=0.0)
        maya.cmds.setKeyframe(tfm, at='rotateX', t=end, v=-5.0)

        # create geometry
        sphere = maya.cmds.polySphere()[0]
        geomSet = mayaUtils.createGeometryAsset(name='sphereGeom1',
                                                geomList=[sphere])

        # create cube rig
        cube = maya.cmds.polyCube()[0]
        ctrl = maya.cmds.circle(nr=(0, 1, 0), radius=2)[0]
        mayaUtils.createRigAsset(name='characterCubeName',
                                 geomList=[cube], ctrlList=[ctrl])
        maya.cmds.setKeyframe(ctrl, at='translateX', t=start, v=-1.0)
        maya.cmds.setKeyframe(ctrl, at='translateX', t=end, v=1.0)
        maya.cmds.setKeyframe(ctrl, at='rotateY', t=start, v=-45.0)
        maya.cmds.setKeyframe(ctrl, at='rotateY', t=end, v=45.0)

        # create shaders
        uvShd, uvShdGrp = mayaUtils.createShaderAsset('uvTest',
                                                      nodeType='lambert',
                                                      color=(0.5, 0.5, 0.5))
        # mayaUtils.assignShaderAsset([cube], uvShdGrp)
        mayaUtils.assignObjectListToShader(objList=[cube], shader=uvShd)
        mayaUtils.assignObjectListToShader(objList=[sphere], shader=uvShd)

        # create uv shader textures
        testUvs = os.path.join(testBaseDir, 'uvTestTexture.jpg')
        uvTx = mayaUtils.createTextureAsset('uvTestTexture1', path=testUvs)
        mayaUtils.connectTextureToShader(uvTx, uvShd, 'color')

    # save scene before test
    mayaUtils.saveTestFile('test8_before')

    # do checks
    lib.run()

    # save the scene
    mayaUtils.saveTestFile('test8_after')
    return


def main():
    print 'Running tests...', __file__
    test1()
    test2()
    test3()
    test4()
    test5()
    test6()
    test7()
    test8()


if __name__ == '__main__':
    main()
    maya.cmds.quit()
