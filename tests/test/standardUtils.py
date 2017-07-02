"""
Utilities to help testing and creation of test scenes.
"""

import os
import json


def _generateFilePath(root, assetType, name, fileName):
    """Generate a file path in the assets directory."""
    return os.path.join(root, assetType, name, fileName)


def _generateAssetFilePath(root, assetType, name):
    """Generate a JSON file path for an asset."""
    return os.path.join(root, assetType, name + '.json')


def _generatePlateFilePath(root, name):
    """Generate a plate path."""
    fileName = 'plate.' + name + '.####.jpg'
    return _generateFilePath(root, 'imageSequence', name, fileName)


def _generateTextureFilePath(root, name):
    """Generate a texture path."""
    fileName = 'texture.' + name + '.jpg'
    return _generateFilePath(root, 'texture', name, fileName)


def _readData(path):
    """Read a JSON file."""
    f = open(path, 'rb')
    data = json.load(f)
    f.close()
    return data


def _writeData(path, data):
    """Write data to a JSON file"""
    f = open(path, 'wb')
    json.dump(data, f)
    f.close()
    return True


def _createFile(data, name, assetType, root):
    """Create file path."""
    path = _generateAssetFilePath(root, assetType, name)
    dirPath = os.path.dirname(path)
    if not os.path.isdir(dirPath):
        os.makedirs(dirPath)
    print 'Creating File:', path
    _writeData(path, data)
    return path


class AssetFile(object):
    """
    Defines an asset file with convenient functions for reading the data.
    """
    def __init__(self, path, name, assetType, ext='json'):
        self.__path = path
        self.__name = name
        self.__type = assetType

    def getName(self):
        return self.__name

    def getType(self):
        return self.__type

    def getPath(self):
        return self.__path

    def getData(self):
        path = self.getPath()
        return _readData(path)

    def setData(self, data):
        path = self.getPath()
        return _writeData(path, data)


def getAssets(root):
    """
    Return a list of assets.

    :param root: Root directory.
    :type root: basestring
    :rtype: list of AssetFiles 
    :return: List of AssetFile class objects.
    """
    assert os.path.isdir(root)
    assetList = []
    assetTypes = os.listdir(root)
    for assetType in assetTypes:
        assetTypePath = os.path.join(root, assetType)
        if os.path.isfile(assetTypePath):
            continue
        assetNames = os.listdir(assetTypePath)
        for assetName in assetNames:
            assetNamePath = os.path.join(assetTypePath, assetName)
            if assetNamePath not in assetList:
                assetName, formatExt = os.path.splitext(assetName)
                asset = AssetFile(assetNamePath, assetName, assetType)
                assetList.append(asset)
    return assetList


def createGenericAsset(name='generic1', root=None, data=None):
    assert name
    assert root
    assert data and isinstance(data, dict)
    assetType = 'generic'
    path = _createFile(data, name, assetType, root)
    return AssetFile(path, name, assetType)


def createImageSequenceAsset(name='imgSeq1', root=None, data=None):
    assert name
    assert root
    assert data and isinstance(data, dict)
    assetType = 'imageSequence'
    path = _createFile(data, name, assetType, root)
    return AssetFile(path, name, assetType)


def createCameraAsset(name='camera1', root=None, data=None):
    assert name
    assert root
    assert data and isinstance(data, dict)
    assetType = 'camera'
    path = _createFile(data, name, assetType, root)
    return AssetFile(path, name, assetType)


def createGeometryAsset(name='geom1', root=None, data=None):
    assert name
    assert root
    assert data and isinstance(data, dict)
    assetType = 'geometry'
    path = _createFile(data, name, assetType, root)
    return AssetFile(path, name, assetType)


def createRigAsset(name='rig1', root=None, data=None):
    assert name
    assert root
    assert data and isinstance(data, dict)
    assetType = 'rig'
    path = _createFile(data, name, assetType, root)
    return AssetFile(path, name, assetType)


def createShaderAsset(name='shader1', root=None, data=None):
    assert name
    assert root
    assert data and isinstance(data, dict)
    assetType = 'shader'
    data = {}
    path = _createFile(data, name, assetType, root)
    return AssetFile(path, name, assetType)


def createTextureAsset(name='texture1', root=None, data=None):
    assert name
    assert root
    assert data and isinstance(data, dict)
    assetType = 'texture'
    path = _createFile(data, name, assetType, root)
    return AssetFile(path, name, assetType)


def createBasicTextureAsset(name=None, mode=None, root=None):
    name = name + '.' + mode
    path = _generateTextureFilePath(root, name)
    data = {
        'path': path,
        'mode': mode,
    }
    return createTextureAsset(name=name, root=root, data=data)


def createPlateAsset(name=None, root=None):
    path = _generatePlateFilePath(name, root)
    data = {'path': path}
    return createImageSequenceAsset(name=name, root=root, data=data)


def createRenderCameraAsset(name='renderCamera', root=None):
    data = {
        'translateX': [(1, 0.0), (24, 10.0)],
        'translateY': [(1, -10.0), (24, 2.0)],
        'translateZ': [(1, 0.0), (24, 0.0)],

        'rotateX': [(1, -5.0), (24, 25.0)],
        'rotateY': [(1, -10.0), (24, 10.0)],
        'rotateZ': [(1, 0.0), (24, 0.0)],

        'focalLength': 50.0,
        'filmBackWidth': 36.0,
        'filmBackHeight': 24.0,
    }
    return createCameraAsset(data=data, name=name, root=root)


def createTrackCameraAsset(name='trackCamera', subName=None, root=None):
    assert subName and isinstance(subName, basestring)
    name = name + '.' + subName
    plateAsset = createPlateAsset(name=name, root=root)
    platePath = plateAsset.getPath()
    data = {
        'translateX': [(1, 0.0), (24, 10.0)],
        'translateY': [(1, -10.0), (24, 2.0)],
        'translateZ': [(1, 0.0), (24, 0.0)],

        'rotateX': [(1, -5.0), (24, 25.0)],
        'rotateY': [(1, -10.0), (24, 10.0)],
        'rotateZ': [(1, 0.0), (24, 0.0)],

        'focalLength': 35.0,
        'filmBackWidth': 36.0,
        'filmBackHeight': 24.0,
        'platePath': platePath,
    }
    return createCameraAsset(data=data, name=name, root=root), plateAsset


def createSphereGeomAsset(name='sphereGeom1', root=None, data=None):
    data = {
        'shapes': ['pSphereShape1'],
        'faceNum': 400,
        'vertNum': 360
    }
    return createGeometryAsset(data=data, name=name, root=root)


def createCharacterRigAsset(name='charRig1', root=None, data=None):
    data = {
        'controls': ['world_CTRL'],
        'meshes': ['pSphereShape1'],
    }
    return createRigAsset(data=data, name=name, root=root)


def createMetalShaderAsset(name='metalShd1', root=None, data=None):
    texName = 'metal'
    diffTex = createBasicTextureAsset(name=texName, mode='diffuse', root=root)
    specTex = createBasicTextureAsset(name=texName, mode='specular', root=root)
    bumpTex = createBasicTextureAsset(name=texName, mode='bump', root=root)
    data = {
        'diffuseLevel': 0.1,
        'specularLevel': 0.9,
        'diffuseTexture': diffTex.getPath(),
        'specularTexture': specTex.getPath(),
        'bumpTexture': bumpTex.getPath(),
    }
    return createShaderAsset(data=data, name=name, root=root), diffTex, specTex, bumpTex


def createWoodShaderAsset(name='woodShd1', root=None, data=None):
    texName = 'wood'
    diffTex = createBasicTextureAsset(name=texName, mode='diffuse', root=root)
    specTex = createBasicTextureAsset(name=texName, mode='specular', root=root)
    bumpTex = createBasicTextureAsset(name=texName, mode='bump', root=root)
    data = {
        'diffuseLevel': 0.4,
        'specularLevel': 0.2,
        'diffuseTexture': diffTex.getPath(),
        'specularTexture': specTex.getPath(),
        'bumpTexture': bumpTex.getPath(),
    }
    return createShaderAsset(data=data, name=name, root=root), diffTex, specTex, bumpTex
