"""
Gathers rig assets from the current scene.
"""

import maya.cmds

import assetQC.api.register as register
import assetQC.api.collector as collector
import assetQC.api.context as context
import test.mayaAssets.rig.rigInstance


RIG_PREFIX = 'RIG_'
CTRL_PREFIX = 'CTRL_'
GEOM_PREFIX = 'GEOM_'


def getSet(node, prefix):
    sets = maya.cmds.sets(node, query=True)
    if not sets:
        return None
    tmpSets = list(sets)
    sets = []
    for ctrlSet in tmpSets:
        if maya.cmds.nodeType(ctrlSet) != 'objectSet':
            continue
        if str(ctrlSet).startswith(prefix):
            sets.append(str(ctrlSet))
    if sets:
        return sets[0]
    return None


class RigCollector(collector.Collector):
    enable = True
    priority = 2
    assetTypes = ['rig']
    hostApps = ['maya']

    def condition(self, ctx):
        return True

    def run(self, ctx):
        assert isinstance(ctx, context.Context)
        nodes = maya.cmds.ls(sets=True, long=True)
        for node in nodes:
            nodePathSplit = node.split('|')
            nodeSplit = nodePathSplit[-1].split('_')

            if not node.startswith(RIG_PREFIX):
                continue

            name = str('_'.join(nodeSplit[1:]))
            instance = test.mayaAssets.rig.rigInstance.RigInstance(name)
            ctx.addInstance(instance)
            instance.setNode(str(node))
            instance.setRigSetNode(str(node))

            ctrlSet = getSet(node, CTRL_PREFIX)
            if ctrlSet:
                instance.setControlsSetNode(ctrlSet)
            else:
                continue

            geoSet = getSet(node, GEOM_PREFIX)
            if geoSet:
                instance.setGeometrySetNode(geoSet)
            else:
                continue
        return

manager = register.getPluginManager()
manager.registerPlugin(RigCollector)
