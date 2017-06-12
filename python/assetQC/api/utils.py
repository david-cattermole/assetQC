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
