"""
Low-level utilities for the 'check asset' tool.

Intended to be used for internal use ONLY.
"""

import os
import sys

import assetQC.api.logger

HOST_APP_ALL = 'all'
HOST_APP_STANDALONE = 'standalone'
HOST_APP_MAYA = 'maya'


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
    Print a progress number to the log. 
    """
    if progressCb:
        progressCb(msg, num)
    elif logger is not None:
        assert isinstance(logger, assetQC.api.logger.AssetQCLogger)
        logger.progress(msg, num)


def printProgress(msg, index, total, minNum, maxNum, progressCb):
    """
    Print a progress number to the log.
    
    :param msg: Text for the progress. For example the 'step' that has progress.
    :param index: 
    :param total: 
    :param minNum: 
    :param maxNum: 
    :param progressCb: 
    :return: 
    """
    num = progressNum(index, total, minNum, maxNum)
    if not progressCb:
        logger = assetQC.api.logger.getLogger()
        progressCb = logger.progress
    progressCb(msg, num)


def formatInstances(context, validFilter):
    """
    Returns information about all instances and their validity. 
    
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
    """
    Determines if we are running inside Autodesk Maya.

    :return: True or False. 
    """
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
    """
    Determines if we are running inside the standalone Python interpreter.

    :return: True or False. 
    """
    result = False
    if sys.executable:
        dir, name = os.path.split(sys.executable)
        if 'python' in name:
            result = True
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
