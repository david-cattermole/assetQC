"""
Context of the testing environment.

Stores the following:
- Job, Sequence, Shot
- User
- Date, Time
- Running Host Application
- Computer Host Name (???)
- Asset Instances objects (???)
- Collector objects (???)
- Validator objects (???)
- etc.
"""

import os
import pwd
import socket
import assetQC.api.utils
import assetQC.api.assetInstance
import assetQC.api.baseDataObject

# Find Modes
FIND_MODE_COLLECTORS = 'COLLECTORS'
FIND_MODE_VALIDATORS = 'VALIDATORS'
FIND_MODE_REPORTERS = 'REPORTERS'
FIND_MODE_ALL = (FIND_MODE_COLLECTORS,
                 FIND_MODE_VALIDATORS,
                 FIND_MODE_REPORTERS)
FIND_MODE_NONE = ()


class Context(assetQC.api.baseDataObject.BaseDataObject):
    """
    Defines the Context ('state') the 'assetQC' process is executed in.
    
    'Context' is used to hold plugins and Asset Instances to be operated on by 
    the 'assetQC' process.    
    
    Allows read-only access to system information.
    """

    def __init__(self,
                 find=None):
        super(Context, self).__init__()

        # user data
        self.__environ = dict(os.environ)
        self.__operatingSystem = os.name
        self.__userName = pwd.getpwuid(os.geteuid()).pw_name
        self.__hostName = socket.gethostname()
        # TODO: We should add the ability to detect and extend 'hostApps'.
        self.__hostApplication = 'maya'  # None

        # plugins
        self.__collectors = []
        self.__validators = []
        self.__reporters = []

        # mayaAssets
        self.__instances = {}

        # find objects
        if find is None:
            find = FIND_MODE_ALL
        if FIND_MODE_COLLECTORS in find:
            self.findCollectorPlugins()
        if FIND_MODE_VALIDATORS in find:
            self.findValidatorPlugins()
        if FIND_MODE_REPORTERS in find:
            self.findReporterPlugins()

    def getEnvVar(self, name, default=None):
        return self.__environ.get(name, default)

    def getUserName(self):
        return self.__userName

    def getUserEmailAddress(self):
        name = self.getUserName()
        host = self.getHostName()
        return '{0}@{1}'.format(name, host)

    def getHostApp(self):
        return self.__hostApplication

    def getHostName(self):
        return self.__hostName

    def getInstances(self,
                     sortByName=False,
                     sortByDataKeyword=False,
                     dataKeyword=None):
        instances = []
        if not sortByName:
            for name in self.__instances:
                instances.append(self.__instances[name])

        if sortByName:
            # sort by asset type and name
            instanceNames = {}
            for name in self.__instances:
                instance = self.__instances[name]
                aType = instance.getAssetType()
                key = aType + '_' + name
                instanceNames[key] = instance
            instances = []
            for key in sorted(instanceNames):
                instances.append(instanceNames[key])

        elif sortByDataKeyword:
            # sort by arbitrary keyword
            instanceNames = {}
            for instance in instances:
                key = instance.data[dataKeyword]
                instanceNames[key] = instance
            instances = []
            for key in sorted(instanceNames):
                instances.append(instanceNames[key])
        return instances

    def hasInstance(self, name):
        if name in self.__instances:
            return True
        return False

    def addInstances(self, values):
        for value in values:
            assert isinstance(value, assetQC.api.assetInstance.AssetInstance)
            self.__instances.append(value)

    def addInstance(self, value):
        assert isinstance(value, assetQC.api.assetInstance.AssetInstance)
        name = value.getName()
        if not self.hasInstance(name):
            self.__instances[name] = value
        return True

    def clearInstances(self):
        self.__instances = {}

    def findCollectorPlugins(self):
        self.__collectors = assetQC.api.utils.findPlugins(self.__collectors,
                                                          'collector')
        return True

    def findValidatorPlugins(self):
        self.__validators = assetQC.api.utils.findPlugins(self.__validators,
                                                          'validator')
        return True

    def findReporterPlugins(self):
        self.__reporters = assetQC.api.utils.findPlugins(self.__reporters,
                                                         'reporter')
        return True

    def getCollectorPlugins(self, assetType=None):
        hostApp = self.getHostApp()
        return assetQC.api.utils.getPlugins(self.__collectors,
                                            assetType=assetType,
                                            hostApp=hostApp)

    def getValidatorPlugins(self, assetType=None):
        hostApp = self.getHostApp()
        return assetQC.api.utils.getPlugins(self.__validators,
                                            assetType=assetType,
                                            hostApp=hostApp)

    def getReporterPlugins(self, assetType=None):
        return assetQC.api.utils.getPlugins(self.__reporters,
                                            assetType=assetType,
                                            hostApp=None)

    def clearCollectorPlugins(self, assetTypes=()):
        self.__collectors = assetQC.api.utils.clearPlugins(self.__collectors,
                                                           assetTypes=assetTypes)
        return True

    def clearValidatorPlugins(self, assetTypes=()):
        self.__validators = assetQC.api.utils.clearPlugins(self.__validators,
                                                           assetTypes=assetTypes)
        return True

    def clearReporterPlugins(self, assetTypes=()):
        self.__reporters = assetQC.api.utils.clearPlugins(self.__reporters,
                                                          assetTypes=assetTypes)
        return True

    def clearAllPlugins(self):
        self.clearCollectorPlugins()
        self.clearValidatorPlugins()
        self.clearReporterPlugins()
        return True

    def addCollectorPlugin(self, collector):
        collectors = self.getCollectorPlugins()
        if collector not in collectors:
            self.__collectors.append(collector)
        return True

    def addValidatorPlugin(self, validator):
        validators = self.getValidatorPlugins()
        if validator not in validators:
            self.__validators.append(validator)
        return True

    def addReporterPlugin(self, reporter):
        reporters = self.getReporterPlugins()
        if reporter not in reporters:
            self.__reporters.append(reporter)
        return True

    def removeCollectorPlugin(self, collector):
        collectors = self.getCollectorPlugins()
        if collector in collectors:
            self.__collectors.remove(collector)
        return True

    def removeValidatorPlugin(self, validator):
        validators = self.getValidatorPlugins()
        if validator in validators:
            self.__validators.remove(validator)
        return True

    def removeReporterPlugin(self, reporter):
        reporters = self.getReporterPlugins()
        if reporter in reporters:
            self.__reporters.remove(reporter)
        return True
