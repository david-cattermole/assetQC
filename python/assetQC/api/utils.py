"""
Low-level utilities for the 'check asset' tool.

Intended to be used for internal use ONLY.
"""

import os
import imp
import sys
import assetQC.api.logger
import assetQC.api.config as config

HOST_APP_ALL = 'all'
HOST_APP_STANDALONE = 'standalone'
HOST_APP_MAYA = 'maya'


def sortObjectsByPriority(objList, assetType):
    """
    
    :param objList: 
    :param assetType: 
    :return: 
    """
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
    """
    
    :return: 
    """
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
    """
    
    :param searchDirectories: 
    :param endswithString: 
    :param extension: 
    :return: 
    """
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
    """
    
    :param pluginList: 
    :param pluginType: 
    :return: 
    """
    searchDirs = getSearchPaths()
    plugins = findPlugin(searchDirs, pluginType)
    for plugin in plugins:
        if plugin not in pluginList:
            pluginList.append(plugin)
    return pluginList


def getPlugins(pluginList, assetType=None, hostApp=None):
    """
    
    :param pluginList: 
    :param assetType: 
    :param hostApp: 
    :return: 
    """
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
    """
    
    :param pluginList: 
    :param assetTypes: 
    :return: 
    """
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
    """
    
    :param index: 
    :param totalNum: 
    :param minNum: 
    :param maxNum: 
    :return: 
    """
    num = float(index + 1) / float(totalNum)
    diffNum = maxNum - minNum
    num = minNum + (num * diffNum)
    return int(round(num))


def printProgressNum(msg, num, progressCb, logger=None):
    """
    
    :param msg: 
    :param num: 
    :param progressCb: 
    :param logger: 
    :return: 
    """
    if progressCb:
        progressCb(msg, num)
    else:
        logger.progress(msg, num, logger=logger)


def printProgress(msg, index, total, minNum, maxNum, progressCb):
    """
    
    :param msg: 
    :param index: 
    :param total: 
    :param minNum: 
    :param maxNum: 
    :param progressCb: 
    :return: 
    """
    num = progressNum(index, total, minNum, maxNum)
    if progressCb:
        progressCb(msg, num)
    else:
        logger.progress(msg, num)


def formatInstances(context, validFilter):
    """
    
    :param context: 
    :param validFilter: 
    :return: 
    """
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


def isMayaRunning():
    result = False

    try:
        import maya.standalone
        maya.standalone.initialize()
        result = True
    except ImportError:
        result = False

    try:
        import maya.cmds
        if maya.cmds.about(version=True):
            result = True
        else:
            result = True
    except:
        result = False
    return result


def isStandaloneRunning():
    result = False
    if sys.executable:
        dir, name = os.path.split(sys.executable)
        if 'python' in name:
            result = True
    # if not isMayaRunning():
    #     result = True
    # assert False
    return result


def getHostApplication():
    result = None
    if assetQC.api.utils.isMayaRunning():
        result = HOST_APP_MAYA
    elif assetQC.api.utils.isStandaloneRunning():
        result = HOST_APP_STANDALONE
    else:
        result = HOST_APP_STANDALONE
    return result
