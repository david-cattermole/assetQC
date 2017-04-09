"""
AssetInstance

- Defines nodes of an asset.
- Used to store data needed in the Validator.
- Stores an asset type to be used for look up of the validation plugin to use.
"""

import assetQC.api.logger as logger
import assetQC.api.baseDataObject as baseDataObject


class AssetInstance(baseDataObject.BaseDataObject):

    def __init__(self, name, assetType=None):
        super(AssetInstance, self).__init__()
        assert isinstance(name, str)
        assert assetType is None or isinstance(assetType, str)
        self.__name = name
        self.__assetType = assetType
        self.__statuses = {}
        self.__fixers = []
        logName = logger.BASE_LOG_NAME + '.' + name
        self.__logger = logger.getLogger(logName)

    def getName(self):
        return self.__name

    def getAssetType(self):
        return self.__assetType

    def isValid(self):
        # Do we have any statuses?
        return not bool(self.__statuses)

    def addStatus(self, value):
        hashValue = value.getHash()
        if hashValue not in self.__statuses:
            self.__statuses[hashValue] = value

    def removeStatus(self, hashValue):
        if hashValue in self.__statuses:
            self.__statuses.pop(hashValue)

    def getStatusList(self):
        statusList = []
        for statusValue in self.__statuses:
            statusObj = self.__statuses[statusValue]
            statusList.append(statusObj)
        return statusList

    def clearStatusList(self):
        self.__statuses = []

    def addFixer(self, validator, value):
        value = (validator, value)
        if value not in self.__fixers:
            self.__fixers.append(value)

    def addFixers(self, validator, values):
        isinstance(values, list)
        for value in values:
            self.addFixer(validator, value)

    def getFixerList(self):
        return self.__fixers

    def logInfo(self, msg):
        return self.__logger.info(msg)

    def logProgress(self, msg, num):
        msg = '{0}% {1}'.format(num, msg)
        return self.__logger.log(logger.LEVEL_PROGRESS, msg)

    def logWarning(self, msg):
        return self.__logger.warning(msg)

    def logFailure(self, msg):
        return self.__logger.log(logger.LEVEL_FAILURE, msg)

    def logError(self, msg):
        return self.__logger.error(msg)

    def logDebug(self, msg):
        return self.__logger.debug(msg)
