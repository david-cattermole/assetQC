"""
Utilities to help testing and creation of test scenes.
"""

import os
import json


def __createFile(data, name, assetType, root):
    path = os.path.join(root, assetType, name + '.json')
    dirPath = os.path.dirname(path)
    if not os.path.isdir(dirPath):
        os.makedirs(dirPath)
    print 'Creating File:', repr(path)
    f = open(path, 'wb')
    json.dump(data, f)
    f.close()
    return path


def listAssets(root):
    assert os.path.isdir(root)
    result = {}
    assetTypes = os.listdir(root)
    for assetType in assetTypes:
        assetTypePath = os.path.join(root, assetType)
        assetNames = os.listdir(assetTypePath)
        for assetName in assetNames:
            assetNamePath = os.path.join(assetTypePath, assetName)
            if assetNamePath not in result:
                assetName, formatExt = os.path.splitext(assetName)
                result[assetNamePath] = {'type': assetType,
                                         'name': assetName,
                                         'ext': formatExt}
    return result


def createCameraAsset(name='camera1', root=None, data=None):
    assert name
    assert root
    assert data and isinstance(data, dict)
    assetType = 'camera'
    return __createFile(data, name, assetType, root)


def createGeometryAsset(name='geom1', root=None, data=None):
    assert name
    assert root
    assert data and isinstance(data, dict)
    assetType = 'geometry'
    return __createFile(data, name, assetType, root)


def createRigAsset(name='rig1', root=None, data=None):
    assert name
    assert root
    assert data and isinstance(data, dict)
    assetType = 'rig'
    return __createFile(data, name, assetType, root)


def createShaderAsset(name='shader1', root=None, data=None):
    assert name
    assert root
    assert data and isinstance(data, dict)
    assetType = 'shader'
    data = {}
    return __createFile(data, name, assetType, root)


def createTextureAsset(name='texture1', root=None, data=None):
    assert name
    assert root
    assert data and isinstance(data, dict)
    assetType = 'texture'
    return __createFile(data, name, assetType, root)
