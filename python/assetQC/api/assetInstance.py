"""
AssetInstance

- Defines nodes of an asset.
- Used to store data needed in the Validator.
- Stores an asset type to be used for look up of the validation plugin to use.
"""

import assetQC.api.logger
import assetQC.api.baseDataObject as baseDataObject


class AssetInstance(baseDataObject.BaseDataObject):
    """
    Defines an asset.
    """
    priority = 1
    enable = True
    
    def __init__(self, name, assetType=None):
        super(AssetInstance, self).__init__()
        assert isinstance(name, str) and name
        assert assetType is None or isinstance(assetType, str)
        self.__name = name
        self.__assetType = assetType
        self.__statuses = {}
        self.__fixers = []
        logName = assetQC.api.logger.BASE_LOG_NAME + '.' + name
        self.__logger = assetQC.api.logger.getLogger(logName)

    def getName(self):
        """
        Return the name of the AssetInstance 
        """
        return self.__name

    def getAssetType(self):
        """
        Returns the asset type of the AssetInstance. 
        """
        return self.__assetType

    def isValid(self):
        """
        Returns the state of the AssetInstance validation.

        The AssetInstance is not valid if there are any error messages logged 
        against the AssetInstance.
        """
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
        """
        Return list of Fixer objects attached to this AssetInstance.
        """
        return self.__fixers

    def logInfo(self, msg):
        """
        Log an information message against this AssetInstance object.

        :param msg: Message to log.
        :type msg: str
        :return: None
        """
        return self.__logger.info(msg)

    def logProgress(self, msg, num):
        """
        Log a progress message against this AssetInstance object.

        :param msg: Message to log.
        :type msg: str
        :param num: Percentage of the progress, between 0 and 100 inclusive.
        :type num: int
        :return: None
        """
        msg = '{0}% {1}'.format(num, msg)
        return self.__logger.log(assetQC.api.logger.LEVEL_PROGRESS, msg)

    def logWarning(self, msg):
        """
        Log a warning message against this AssetInstance object.

        :param msg: Message to log.
        :type msg: str
        :return: None
        """
        return self.__logger.warning(msg)

    def logFailure(self, msg):
        """
        Log a failure message against this AssetInstance object.

        :param msg: Message to log.
        :type msg: str
        :return: None
        """
        return self.__logger.log(assetQC.api.logger.LEVEL_FAILURE, msg)

    def logError(self, msg):
        """
        Log an error message against this AssetInstance object.

        :param msg: Message to log.
        :type msg: str
        :return: None
        """
        return self.__logger.error(msg)

    def logDebug(self, msg):
        """
        Log a debug message against this AssetInstance object.

        :param msg: Message to log.
        :type msg: str
        :return: None
        """
        return self.__logger.debug(msg)
