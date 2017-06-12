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

import assetQC.api.register
import assetQC.api.utils
import assetQC.api.assetInstance
import assetQC.api.baseDataObject


class Context(assetQC.api.baseDataObject.BaseDataObject):
    """
    Defines the Context ('state') the 'assetQC' process is executed in.
    
    'Context' is used to hold plugins and Asset Instances to be operated on by 
    the 'assetQC' process.    
    
    Allows read-only access to system information.
    """

    def __init__(self,
                 pluginManager=None,
                 root=None,
                 hostApp=None):
        super(Context, self).__init__()
        assert root is None or isinstance(root, str)
        assert hostApp is None or isinstance(hostApp, str)

        # user data
        self.__environ = dict(os.environ)
        self.__operatingSystem = os.name
        self.__userName = pwd.getpwuid(os.geteuid()).pw_name
        self.__hostName = socket.gethostname()
        self.__hostApplication = assetQC.api.utils.HOST_APP_ALL
        if hostApp is None:
            self.__hostApplication = assetQC.api.utils.getHostApplication()
        elif hostApp:
            self.__hostApplication = hostApp
        self.__rootDirectory = os.getcwd()
        if root:
            self.__rootDirectory = root

        # plugins
        self.__pluginManager = None
        if isinstance(pluginManager, assetQC.api.register.PluginManager):
            self.__pluginManager = pluginManager
        else:
            self.__pluginManager = assetQC.api.register.getPluginManager()
            assetQC.api.register.importAllPlugins()

        # assets
        self.__instances = {}

    def getEnvVar(self, name, default=None):
        return self.__environ.get(name, default)

    def getRootDirectory(self):
        return self.__rootDirectory

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

    def getPluginManager(self):
        return self.__pluginManager

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
            self.addInstance(value)

    def addInstance(self, value):
        assert isinstance(value, assetQC.api.assetInstance.AssetInstance)
        name = value.getName()
        if not self.hasInstance(name):
            self.__instances[name] = value
        return True

    def clearInstances(self):
        self.__instances = {}
