"""
Gathers geometry assets from the current scene.
"""

import maya.cmds

import assetQC.api.register as register
import assetQC.api.collector as collector
import assetQC.api.context as context
import test.mayaAssets.geometry.geometryInstance

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


class GeometryCollector(collector.Collector):
    enable = True
    priority = 3
    assetTypes = ['geometry']
    hostApps = ['maya']

    def condition(self, ctx):
        return True

    def run(self, ctx):
        assert isinstance(ctx, context.Context)
        maya.cmds.ls()
        nodes = maya.cmds.ls(sets=True, long=True)
        for node in nodes:
            if not node.startswith(GEOM_PREFIX):
                continue

            geomList = maya.cmds.sets(node, query=True) or []
            name = str(node)[len(GEOM_PREFIX):]
            instance = test.mayaAssets.geometry.geometryInstance.GeometryInstance(name)
            instance.setNode(str(node))
            instance.setGeometryList(geomList)
            ctx.addInstance(instance)
        return True

manager = register.getPluginManager()
manager.registerPlugin(GeometryCollector)
