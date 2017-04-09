"""
Gathers camera assets from the current scene.
"""

import os
import maya.cmds
import assetQC.api.collector as collector
import assetQC.api.context as context
import assetQC.test.mayaAssets.texture.textureInstance as textureInstance

TEXTURE_EXTENSIONS = ['png', 'jpeg', 'jpg', 'tga', 'bmp',
                      'exr', 'tif', 'tiff', 'hdr']


class TextureCollector(collector.Collector):
    enable = True
    priority = 4
    assetTypes = ['texture']
    hostApps = ['maya']

    def condition(self, ctx):
        return True

    def run(self, ctx):
        assert isinstance(ctx, context.Context)
        nodes = maya.cmds.ls(textures=True)
        for node in nodes:
            if not node.startswith('TX_'):
                continue

            attrs = maya.cmds.listAttr(node, hasData=True) or []
            for attr in attrs:
                if '.' in attr:
                    continue
                nodeAttr = node + '.' + attr
                if 'colorSpace' == attr:
                    continue

                # attr type
                attrType = maya.cmds.getAttr(nodeAttr, type=True)
                if attrType != 'string':
                    continue

                # attr value
                value = maya.cmds.getAttr(nodeAttr)
                if not value:
                    continue

                # asset name
                basePath, fileName = os.path.split(value)
                split = fileName.split('.')
                name = fileName
                if len(split) > 1:
                    name = '_'.join(split[:-1]) + '_' + str(split[-1]).upper()

                instance = textureInstance.TextureInstance(str(name))
                instance.setNode(str(node))
                instance.setAttr(str(attr))
                instance.setNodeAttr(str(nodeAttr))
                instance.setDirectory(str(basePath))
                instance.setFilePath(str(value))
                instance.setFileName(str(fileName))
                ctx.addInstance(instance)
        return True
