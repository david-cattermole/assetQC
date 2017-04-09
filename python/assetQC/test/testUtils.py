"""
Utilties to help testing and creation of test scenes.
"""

import os
import maya.cmds
import assetQC.api.config as config


def saveTestFile(name):
    testTempDir = config.getTestTempDir()
    filePath = os.path.join(testTempDir, '%s.ma' % name)
    print '=' * 40
    print 'Saving File:', filePath
    maya.cmds.file(rename=filePath)
    return maya.cmds.file(save=True, force=True, type='mayaAscii')


def getLongNameOf(node):
    """Return the full path to the node given.

    :param node: Node path.
    :__type node: str or unicode

    :return: str or unicode, the full path to the node.
    """
    result = maya.cmds.ls(node, long=True)
    if result and len(result):
        return result[0]
    return None


def reinitializeScene(frameRange=None):
    maya.cmds.file(new=True, force=True)
    if frameRange:
        startFrame = int(frameRange[0])
        endFrame = int(frameRange[1])
        maya.cmds.playbackOptions(minTime=startFrame, maxTime=endFrame)
        maya.cmds.playbackOptions(animationStartTime=startFrame,
                                  animationEndTime=endFrame)
    return


def createCameraAsset(name='camera1'):
    camTfm = getLongNameOf(maya.cmds.createNode('transform',
                                                name=name))
    camShp = getLongNameOf(maya.cmds.createNode('camera',
                                                parent=camTfm))
    maya.cmds.setAttr(camShp + '.displayFilmGate', 1)
    maya.cmds.setAttr(camShp + '.overscan', 1.3)
    maya.cmds.setAttr(camShp + '.shutterAngle', 180.0)
    maya.cmds.setAttr(camShp + '.displayCameraFrustum', 1)
    return camTfm, camShp


def createGeometryAsset(name='geom1', geomList=None):
    # ensure we have some geom.
    assert isinstance(geomList, list)

    # get geom list
    geomTfmList = []
    for geom in geomList:
        tfmList = maya.cmds.ls(geom, long=True)
        for tfm in tfmList:
            if tfm not in geomTfmList:
                geomTfmList.append(tfm)

    # Geometry
    geomSetName = 'GEOM_{0}'.format(name)
    geomSet = maya.cmds.sets(geomTfmList, name=geomSetName)
    return geomSet


def createRigAsset(name='rig1', ctrlList=None, geomList=None):
    # ensure we have some geom.
    if geomList is None:
        geom = maya.cmds.polySphere()[0]
        geomList = [geom]
    assert isinstance(geomList, list)

    # ensure we have some controls.
    if ctrlList is None:
        ctrl = maya.cmds.circle(nr=(0, 1, 0), radius=2)[0]
        ctrlList = [ctrl]
    assert isinstance(ctrlList, list)

    # create ctrl list
    ctrlTfmList = []
    for ctrl in ctrlList:
        tfmList = maya.cmds.ls(ctrl, long=True) or []
        for tfm in tfmList:
            if tfm not in ctrlTfmList:
                ctrlTfmList.append(tfm)

    # Controls
    ctrlsSetName = 'CTRL_{0}'.format(name)
    ctrlsSet = maya.cmds.sets(name=ctrlsSetName)
    for tfm in ctrlTfmList:
        assert maya.cmds.objExists(tfm)
        maya.cmds.sets(tfm, edit=True, forceElement=ctrlsSet)

    # create geom list
    geomTfmList = []
    for geom in geomList:
        tfmList = maya.cmds.ls(geom, long=True) or []
        for tfm in tfmList:
            if tfm not in geomTfmList:
                geomTfmList.append(tfm)

    # Geometry
    geomSetName = 'GEOM_{0}'.format(name)
    geomSet = maya.cmds.sets(name=geomSetName)
    for tfm in geomTfmList:
        assert maya.cmds.objExists(tfm)
        maya.cmds.sets(tfm, edit=True, forceElement=geomSet)

    # reparent the geometry under the control
    for geom in geomTfmList:
        maya.cmds.parent(geom, ctrlTfmList[0])

    # Rig
    rigSetName = 'RIG_{0}'.format(name)
    rigSet = maya.cmds.sets([ctrlsSet, geomSet], name=rigSetName)

    return rigSet, ctrlsSet, geomSet


def createShaderAsset(name='shader1', nodeType='lambert', color=None):
    if color:
        assert isinstance(color, list) or isinstance(color, tuple)
    shdName = name
    prefix = 'SHD_'
    if not name.startswith(prefix):
        shdName = prefix + name
    else:
        # remove 'SHD_' if given
        name = name[-len(prefix):]
    shdGrpName = 'SG_' + name

    shd = maya.cmds.shadingNode(nodeType, asShader=True, name=shdName)
    shdGrp = maya.cmds.sets(renderable=True,
                            noSurfaceShader=True,
                            empty=True,
                            name=shdGrpName)

    # # Connect the material to the shading group
    # maya.cmds.defaultNavigation(connectToExisting=True,
    #                             quiet=True, force=True, ignore=True,
    #                             source=shd, destination=shdGrp)
    maya.cmds.connectAttr('%s.outColor' % shd, '%s.surfaceShader' % shdGrp)

    attrs = maya.cmds.listAttr(shd) or []
    colorAttr = None
    if 'color' in attrs:
        colorAttr = 'color'
    elif 'diffuse' in attrs:
        colorAttr = 'diffuse'
    if colorAttr:
        attrType = maya.cmds.getAttr(shd + '.' + colorAttr, type=True)
        if attrType.endswith('3'):
            # only supports 'float3' or 'double3'.
            maya.cmds.setAttr(shd + '.' + colorAttr,
                              color[0], color[1], color[2],
                              type=attrType)

    return shd, shdGrp


def assignShaderAsset(nodes, shdGrp):
    # sel = maya.cmds.ls(sl=True, long=True)
    #
    # maya.cmds.select(nodes, replace=True)
    # maya.cmds.hyperShade(assign=shdGrp)
    #
    # maya.cmds.select(sel, replace=True)

    # Connect sets
    for node in nodes:
        maya.cmds.sets(node, edit=True, forceElement=shdGrp)
    return True


def getSGfromShader(shader=None):
    if shader:
        if maya.cmds.objExists(shader):
            sgq = maya.cmds.listConnections(shader,
                                            destination=True, exactType=True,
                                            type='shadingEngine')
            if sgq:
                return sgq[0]

    return None


def assignObjectListToShader(objList, shader):
    """
    Assign the shader to the object list
    arguments:
        objList: list of objects or faces
    """
    # assign selection to the shader
    shaderSG = getSGfromShader(shader)
    if objList:
        if shaderSG:
            maya.cmds.sets(objList, e=True, forceElement=shaderSG)
        else:
            print 'The provided shader didn\'t returned a shaderSG'
    else:
        print 'Please select one or more objects'


def createTextureAsset(name='texture1', nodeType='file', path=None):
    txName = name
    prefix = 'TX_'
    if not name.startswith(prefix):
        txName = prefix + name

    txNode = maya.cmds.shadingNode(nodeType, asTexture=True, name=txName)

    attrs = maya.cmds.listAttr(txNode, hasData=True) or []
    pathAttr = None
    if 'fileTextureName' in attrs:
        pathAttr = 'fileTextureName'
    if pathAttr:
        maya.cmds.setAttr(txNode + '.' + pathAttr, path, type='string')

    return txNode


def connectTextureToShader(textureNode, shader, shaderAttr):
    shaderNodeAttr = shader + '.' + shaderAttr
    maya.cmds.connectAttr('%s.outColor' % textureNode, shaderNodeAttr)
    return
