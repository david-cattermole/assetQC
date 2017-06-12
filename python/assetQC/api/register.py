import imp
import os

from assetQC.api import config as config
from assetQC.api.utils import HOST_APP_ALL

# module level manager, stores an instance of 'PluginManager'.
__pluginManager = None
__importedModules = []


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


class PluginManager(object):
    def __init__(self):
        self.__plugins = {}

    def registerPlugin(self, classObj):
        if str(classObj) not in self.__plugins:
            self.__plugins[str(classObj)] = classObj
        return True

    def getPlugins(self,
                   classType=object,
                   assetType=None,
                   hostApp=None):
        pluginList = self.__getPluginList()

        # Filter out sub-classes of type 'classType'.
        tmpList = pluginList
        pluginList = []
        for plugin in tmpList:
            if callable(plugin) and issubclass(plugin, classType):
                pluginList.append(plugin)

        # Sort the plug-is based on priority.
        pluginDict = {}
        for plugin in pluginList:
            priority = plugin.priority
            if priority not in pluginDict:
                pluginDict[priority] = [plugin]
            else:
                pluginDict[priority].append(plugin)

        # Filter plugins based on hostApp and enabled status.
        pluginList = []
        for key in sorted(pluginDict.iterkeys()):
            plugins = pluginDict[key]
            for plugin in plugins:
                # Only plugins with a specific 'assetType'.
                if assetType is not None and assetType not in plugin.assetTypes:
                    continue

                # is the plugin enabled?
                if not plugin.enable:
                    continue

                # check if host application is supported by the plugin
                if hostApp and hostApp != HOST_APP_ALL:
                    if hostApp not in plugin.hostApps:
                        continue

                # add the plugin
                pluginList.append(plugin)

        return pluginList

    def __getPluginList(self):
        pluginList = []
        for key in self.__plugins:
            plugin = self.__plugins[key]
            pluginList.append(plugin)
        return pluginList


def importAllPlugins(extension='.py'):
    searchDirs = getSearchPaths()
    assert isinstance(searchDirs, list)

    for searchDir in searchDirs:
        fileNameList = os.listdir(searchDir)

        for fileName in fileNameList:
            name, ext = os.path.splitext(fileName)
            if ext != extension:
                continue

            findMod = imp.find_module(name, [searchDir])
            if not findMod:
                continue

            # Imports all modules in the search directories. Each module is
            # expected to register it's own class, so we don't need to
            # parse the imported module.
            # print 'Importing:', fileName
            try:
                mod = imp.load_module(name, findMod[0], findMod[1], findMod[2])
                # NOTE: We need to add the loaded module into a global variable
                # so that the Python Garbage collector doesn't delete the
                # module, because we might run code in the module some time.
                __importedModules.append(mod)
            except ImportError:
                # print 'Failed importing:', name
                pass
    return


def getPluginManager():
    global __pluginManager
    if __pluginManager is None:
        __pluginManager = PluginManager()
    return __pluginManager


