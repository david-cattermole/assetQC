"""
Gathers camera assets from the current scene.
"""

import maya.cmds

import assetQC.api.collector as collector
import assetQC.api.context as context
import assetQC.test.mayaAssets.shader.shaderInstance as shaderInstance

INVALID_NODES = [
    'lambert1',
    'initialShadingGroup',
    'particleCloud1',
    'initialParticleSE',
    'shaderGlow1',

]

SHADER_PREFIX = 'SHD_'


class ShaderCollector(collector.Collector):
    enable = True
    priority = 3
    assetTypes = ['shader']
    hostApps = ['maya']

    def condition(self, ctx):
        return True

    def run(self, ctx):
        assert isinstance(ctx, context.Context)
        maya.cmds.ls()
        nodes = maya.cmds.ls(materials=True) or []
        for node in nodes:
            if node in INVALID_NODES:
                continue
            if not node.startswith(SHADER_PREFIX):
                continue
            attrValues = {}
            attrs = maya.cmds.listAttr(node, read=True, scalar=True) or []
            for attr in attrs:
                if '.' not in attr:
                    attrValues[str(attr)] = maya.cmds.getAttr(node + '.' + attr)
            name = str(node)[len(SHADER_PREFIX):]
            instance = shaderInstance.ShaderInstance(name)
            instance.setNode(str(node))
            instance.setAttrValues(attrValues)
            ctx.addInstance(instance)
        return True
