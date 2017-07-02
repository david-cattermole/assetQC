"""
Gathers anim assets from the current scene.
"""

import maya.cmds

import assetQC.api.register as register
import assetQC.api.collector as collector
import assetQC.api.context as context
import test.mayaAssets.anim.animInstance

CTRL_PREFIX = 'CTRL_'


class AnimCollector(collector.Collector):
    enable = True
    priority = 3
    assetTypes = ['anim']
    hostApps = ['maya']

    def condition(self, ctx):
        return True

    def run(self, ctx):
        assert isinstance(ctx, context.Context)
        ctrlList = []
        nodes = maya.cmds.ls(sets=True, long=True)
        for node in nodes:
            if not str(node).startswith(CTRL_PREFIX):
                continue
            ctrlNodeList = maya.cmds.sets(str(node), query=True) or []
            for ctrlNode in ctrlNodeList:
                curveList = []
                tmpList = maya.cmds.listConnections(
                    ctrlNode,
                    source=True,
                    destination=True,
                    type='animCurve') or []

                for tmp in tmpList:
                    nodeType = maya.cmds.nodeType(tmp)
                    if 'animCurve' in nodeType:
                        curveList.append(tmp)
                if not curveList:
                    continue

                ctrlList = []
                for curve in curveList:
                    tmpList = maya.cmds.listConnections(
                        curve,
                        source=False,
                        destination=True) or []
                    for tmp in tmpList:
                        if tmp not in ctrlList:
                            ctrlList.append(tmp)

                # create instance
                name = str(ctrlNode).split('|')[-1] + '_ANIM'
                instance = test.mayaAssets.anim.animInstance.AnimInstance(name)
                instance.setNode(str(ctrlNode))
                instance.setCurveNodeList(curveList)
                instance.setControlNodeList(ctrlList)
                ctx.addInstance(instance)

        return True

manager = register.getPluginManager()
manager.registerPlugin(AnimCollector)