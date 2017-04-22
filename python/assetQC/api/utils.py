"""
Low-level utilities for the 'check asset' tool.
"""

import os
import imp
import assetQC.api.logger
import assetQC.api.config as config

HOST_APP_ALL = 'all'


def sortObjectsByPriority(objList, assetType):
    sortedData = {}
    for obj in objList:
        if assetType is not None and assetType not in obj.assetTypes:
            continue
        priority = obj.priority
        if priority not in sortedData:
            sortedData[priority] = [obj]
        else:
            sortedData[priority].append(obj)
    return sortedData


def getSearchPaths():
    searchPaths = config.getPluginSearchPath()
    if not searchPaths:
        return []
    tmpPaths = searchPaths.split(os.pathsep)
    searchPaths = []
    for path in tmpPaths:
        if path and os.path.isdir(path):
            searchPaths.append(path)
    return searchPaths


def findPlugin(searchDirectories, endswithString, extension='.py'):
    assert isinstance(searchDirectories, list)
    assert isinstance(endswithString, str)
    endswithNum = len(endswithString)

    plugins = []
    for searchDir in searchDirectories:
        fileNameList = os.listdir(searchDir)

        for fileName in fileNameList:
            name, ext = os.path.splitext(fileName)
            if ext != extension:
                continue
            if not name.lower().endswith(endswithString):
                continue

            startName = name[:1].upper()
            endName = name[1:]
            className = startName + endName

            path = os.path.join(searchDir, fileName)
            findMod = imp.find_module(name, [searchDir])

            mod = imp.load_module(name, findMod[0], findMod[1], findMod[2])
            plugin = getattr(mod, className, None)
            if plugin is not None:
                plugins.append(plugin)
            else:
                msg = 'Class Name is not valid. ' + className
                logger.debug(msg)

    return plugins


def findPlugins(pluginList, pluginType):
    searchDirs = getSearchPaths()
    plugins = findPlugin(searchDirs, pluginType)
    for plugin in plugins:
        if plugin not in pluginList:
            pluginList.append(plugin)
    return pluginList


def getPlugins(pluginList, assetType=None, hostApp=None):
    pluginDict = sortObjectsByPriority(pluginList, assetType)

    # Return the plugins sorted by priority.
    pluginList = []
    for key in sorted(pluginDict.iterkeys()):
        plugins = pluginDict[key]
        for plugin in plugins:
            # is the plugin enabled?
            if not plugin.enable:
                continue

            # check if host application is supported by the plugin
            if hostApp:
                if hostApp != HOST_APP_ALL:
                    if hostApp not in plugin.hostApps:
                        continue

            # add the plugin
            pluginList.append(plugin)
    return pluginList


def clearPlugins(pluginList, assetTypes=()):
    if len(assetTypes):
        tmpList = list(pluginList)
        pluginList = []
        for tmp in tmpList:
            for assetType in assetTypes:
                if assetType not in tmp.assetTypes:
                    pluginList.append(tmp)
    else:
        pluginList = []
    return pluginList


def progressNum(index, totalNum, minNum, maxNum):
    num = float(index + 1) / float(totalNum)
    diffNum = maxNum - minNum
    num = minNum + (num * diffNum)
    return int(round(num))


def printProgressNum(msg, num, progressCb, logger=None):
    if progressCb:
        progressCb(msg, num)
    else:
        logger.progress(msg, num, logger=logger)


def printProgress(msg, index, total, minNum, maxNum, progressCb):
    num = progressNum(index, total, minNum, maxNum)
    if progressCb:
        progressCb(msg, num)
    else:
        logger.progress(msg, num)


def formatInstances(context, validFilter):
    lines = []
    for instance in context.getInstances(sortByName=True):
        if instance.isValid() != validFilter:
            continue
        name = instance.getName()
        aType = instance.getAssetType()
        data = instance.data
        statusList = instance.getStatusList()

        msg = '{status}: {assetType} - {name} {data} {statusList}'
        msgData = {
            'status': None,
            'name': name,
            'assetType': aType,
            'data': data,
            'statusList': statusList,
        }

        if instance.isValid():
            msgData['status'] = 'Passed'
            lines.append(msg.format(**msgData))
        else:
            msgData['status'] = 'Failed'
            lines.append(msg.format(**msgData))

    return lines

