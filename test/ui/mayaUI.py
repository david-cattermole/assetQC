"""
Maya UI for 'checkAssets' toolset.
"""

import os
import pprint
import maya.cmds
import maya.mel
import assetQC.api.lib as lib
import assetQC.api.logger as logger
import assetQC.api.context as context


class MayaUI(object):

    def __init__(self):
        super(MayaUI, self).__init__()
        # values
        self.windowName = 'asset_qc'
        self.windowTitle = 'Asset QC'
        self.windowWidth = 900
        self.windowHeight = 700

        logName = logger.BASE_LOG_NAME + '.mayaui'
        self.__find_mode = [context.FIND_MODE_COLLECTORS]
        self.__context = None
        self.__logger = logger.getLogger(logName)
        self.__itemPaths = {}

        # UI Items.
        self.__window = None
        self.__mainFormLayout = None
        self.__runValidatorsCheckbox = None
        self.__runFixersCheckbox = None
        self.__runReportersCheckbox = None
        self.__processButton = None
        self.__progressBar = None
        self.__treeLister = None
        self.__infoText = None
        self.__logText = None
        
    def getRunValidatorsValue(self):
        value = maya.cmds.checkBox(self.__runValidatorsCheckbox,
                                   query=True, value=True)
        enable = maya.cmds.checkBox(self.__runValidatorsCheckbox,
                                    query=True, enable=True)
        return value and enable
    
    def getRunFixersValue(self):
        value = maya.cmds.checkBox(self.__runFixersCheckbox,
                                 query=True, value=True)
        enable = maya.cmds.checkBox(self.__runFixersCheckbox,
                                    query=True, enable=True)
        return value and enable

    def getRunReportersValue(self): 
        value = maya.cmds.checkBox(self.__runReportersCheckbox,
                                   query=True, value=True)
        enable = maya.cmds.checkBox(self.__runReportersCheckbox,
                                    query=True, enable=True)
        return value and enable

    def getSelectedPath(self):
        path = maya.cmds.treeLister(self.__treeLister,
                                    query=True, resultsPathUnderCursor=True)
        return str(path)

    def progressCb(self, msg, num):
        # TODO: Get progress callback working with new logger system.
        maya.cmds.progressBar(self.__progressBar, edit=True, progress=num)
        msg = '{0}% {1}'.format(num, msg)
        self.__logger.log(logger.LEVEL_PROGRESS, msg)
        msg += os.linesep

        cancelled = maya.cmds.progressBar(self.__progressBar,
                                          query=True, isCancelled=True)
        self.appendLogText(msg)
        if cancelled:
            msg = '{0}% User Aborted the Operation!'.format(num)
            self.__logger.log(logger.LEVEL_PROGRESS, msg)
            msg += os.linesep
            self.appendLogText(msg)
        return

    def runValidatorsCb(self):
        value = self.getRunValidatorsValue()
        maya.cmds.checkBox(self.__runFixersCheckbox,
                           edit=True,
                           enable=value)
        maya.cmds.checkBox(self.__runReportersCheckbox,
                           edit=True,
                           enable=value)
        return

    def runFixersCb(self):
        value = self.getRunFixersValue()
        return

    def runReportersCb(self):
        value = self.getRunReportersValue()
        return

    def resetLogText(self):
        logString = 'Log:' + os.linesep
        maya.cmds.scrollField(self.__logText, edit=True, text=logString)
        return

    def appendLogText(self, msg):
        logString = maya.cmds.scrollField(self.__logText, query=True, text=True)
        logString += msg
        maya.cmds.scrollField(self.__logText, edit=True, text=logString)
        return

    def updateInfoText(self):
        path = self.getSelectedPath()

        pathDefault = '<path>'
        name = '<name>'
        node = '<node>'
        aType = '<asset type>'
        data = '<data>'
        version = '<version>'
        statusList = []
        if path:
            instance = self.__itemPaths[path]
            name = instance.getName()
            aType = instance.getAssetType()
            data = instance.data
            statusList = instance.getStatusList()
            node = instance.getNode()
            maya.cmds.select(node, replace=True, noExpand=True)
        else:
            path = pathDefault

        # General
        infoString = 'Name: {0}'.format(name) + os.linesep
        infoString += 'Asset Type: {0}'.format(aType) + os.linesep
        infoString += 'Node: {0}'.format(node) + os.linesep
        infoString += 'Version: {0}'.format(version) + os.linesep
        infoString += 'Path: /my/path/to/an/asset/v001' + os.linesep
        infoString += 'Date Created: 2016-03-01 14:43' + os.linesep

        # Status and errors list
        if not statusList:
            infoString += os.linesep + 'Status: Passed' + os.linesep
        else:
            infoString += os.linesep + 'Status: Failed' + os.linesep
        for status in statusList:
            msg = status.getMessage()
            infoString += '- ' + str(msg) + os.linesep

        # Data
        infoString += os.linesep
        infoString += 'Data:' + os.linesep
        if isinstance(data, dict):
            for k in sorted(data):
                d = pprint.pformat(data[k], 4, 4, 4)
                infoString += '- {key}: '.format(key=k)
                if isinstance(data[k], dict):
                    infoString += os.linesep + d
                elif isinstance(data[k], list):
                    infoString += os.linesep
                    for value in sorted(data[k]):
                        infoString += '  - {0}'.format(value) + os.linesep
                else:
                    infoString += d
                infoString += os.linesep

        maya.cmds.scrollField(self.__infoText, edit=True, text=infoString)
        return

    def getIcon(self, aType, valid):
        icon = 'sphere.png'
        if aType == 'camera':
            # 'Camera.png'
            icon = 'camera.svg'
        elif aType == 'rig':
            # 'humanIK_CharCtrl.png'
            icon = 'kinJoint.png'
        elif aType == 'shader':
            # 'render_lambert.png'
            icon = 'render_adskMaterial.png'
        elif aType == 'texture':
            # 'textureBakeSet.svg'
            # icon = 'texturePlacement.png'
            icon = 'place2dTexture.svg'
        elif aType == 'geometry':
            # icon = 'polyCube.svg'
            icon = 'polyCube.png'
        elif aType == 'anim':
            icon = 'animCurveTA.svg'
        if not valid:
            # 'SP_MessageBoxWarning.png'
            # 'error.png'
            icon = 'SP_MessageBoxCritical.png'
        return icon

    def getContextItems(self):
        assetTypes = {}
        items = []

        # List status and asset types.
        passedNum = 0
        failedNum = 0
        instances = self.__context.getInstances(sortByName=True)
        for instance in instances:
            aType = instance.getAssetType()
            if aType not in assetTypes:
                assetTypes[aType] = 1
            else:
                assetTypes[aType] += 1

            if instance.isValid():
                passedNum += 1
            else:
                failedNum += 1

        # collectors
        for instance in instances:
            name = instance.getName()
            aType = instance.getAssetType()
            aTypeNum = assetTypes[aType]
            valid = instance.isValid()

            path = 'Collectors/{type} ({typeNum})/{name}'
            path = path.format(type=aType, typeNum=aTypeNum, name=name)
            self.__itemPaths[path] = instance

            icon = self.getIcon(aType, valid)
            cmd = self.updateInfoText
            items.append((path, icon, cmd))

        # validators
        useValidator = maya.cmds.checkBox(self.__runValidatorsCheckbox,
                                          query=True, value=True)
        if useValidator:
            for instance in instances:
                name = instance.getName()
                aType = instance.getAssetType()

                num = 0
                valid = instance.isValid()
                if valid:
                    status = 'Passed'
                    num = passedNum
                else:
                    status = 'Failed'
                    num = failedNum
                path = 'Validators/{status} ({num})/{name}'
                path = path.format(status=status, num=num, name=name)
                self.__itemPaths[path] = instance

                icon = self.getIcon(aType, valid)

                cmd = self.updateInfoText
                items.append((path, icon, cmd))

        return items

    def updateTree(self):
        tree = self.__treeLister
        items = self.getContextItems()
        maya.cmds.treeLister(tree, e=True, clearContents=True)
        maya.cmds.treeLister(tree, e=True, add=items)
        if self.__itemPaths:
            maya.cmds.treeLister(tree, e=True, selectPath='Collectors')
        maya.cmds.treeLister(tree, e=True, expandToDepth=3)
        return

    def updateFindMode(self):
        self.__find_mode = [context.FIND_MODE_COLLECTORS]

        if self.getRunValidatorsValue():
            self.__find_mode.append(context.FIND_MODE_VALIDATORS)

        if self.getRunReportersValue():
            self.__find_mode.append(context.FIND_MODE_REPORTERS)
        return

    def run(self):
        self.resetLogText()

        self.updateFindMode()
        self.__context = context.Context(find=self.__find_mode)

        doValidators = self.getRunValidatorsValue()
        doFixers = self.getRunFixersValue()
        doReporters = self.getRunReportersValue()

        # Run...
        lib.run(ctx=self.__context,
                doCollectors=True,
                doValidators=doValidators,
                doFixers=doFixers,
                doReporters=doReporters,
                progressCb=self.progressCb)

        # Update UI
        self.updateInfoText()
        self.updateTree()
        return

    def gui(self):
        # window creation
        if maya.cmds.window(self.windowName, query=True, exists=True):
            maya.cmds.deleteUI(self.windowName, window=True)
        self.__window = maya.cmds.window(
            self.windowName,
            title=self.windowTitle,
            sizeable=True,
            widthHeight=(self.windowWidth, self.windowHeight))

        monoSpaceFont = 'fixedWidthFont'
        self.__mainFormLayout = maya.cmds.formLayout(numberOfDivisions=100)
        self.__runValidatorsCheckbox = maya.cmds.checkBox(
            label='Run Validators',
            value=True,
            changeCommand=(lambda x: self.runValidatorsCb()))
        self.__runFixersCheckbox = maya.cmds.checkBox(
            label='Run Fixers',
            value=False,
            changeCommand=(lambda x: self.runFixersCb()))
        self.__runReportersCheckbox = maya.cmds.checkBox(
            label='Run Reporters',
            value=False,
            changeCommand=(lambda x: self.runReportersCb()))
        self.__processButton = maya.cmds.button(
            label='Run...',
            command=(lambda x: self.run()))
        self.__progressBar = maya.cmds.progressBar(minValue=0, maxValue=100)
        self.__treeLister = maya.cmds.treeLister()
        self.__infoText = maya.cmds.scrollField(
            wordWrap=True,
            editable=False,
            font=monoSpaceFont)
        self.__logText = maya.cmds.scrollField(
            wordWrap=True,
            editable=False,
            font=monoSpaceFont)

        spacing = 5
        maya.cmds.formLayout(
            self.__mainFormLayout, edit=True,
            attachControl=[
                (self.__runFixersCheckbox, 'top', spacing, self.__runValidatorsCheckbox),
                (self.__runReportersCheckbox, 'top', spacing, self.__runFixersCheckbox),
                (self.__processButton, 'top', spacing, self.__runReportersCheckbox),
                (self.__progressBar, 'top', spacing, self.__runReportersCheckbox),
                (self.__progressBar, 'left', spacing, self.__processButton),

                (self.__treeLister, 'top', spacing, self.__processButton),
                (self.__treeLister, 'bottom', spacing, self.__logText),
                (self.__infoText, 'top', spacing, self.__progressBar),
                (self.__infoText, 'left', spacing, self.__treeLister),
                (self.__infoText, 'bottom', spacing, self.__logText),
            ],
            attachPosition=[
                (self.__treeLister, 'right', spacing, 45),
                (self.__logText, 'top', spacing, 70),
            ],
            attachForm=[
                (self.__runValidatorsCheckbox, 'top', spacing),
                (self.__progressBar, 'left', spacing),
                (self.__progressBar, 'right', spacing),

                (self.__treeLister, 'left', spacing),
                (self.__infoText, 'right', spacing),

                (self.__logText, 'bottom', spacing),
                (self.__logText, 'left', spacing),
                (self.__logText, 'right', spacing)
            ]
        )

        # self.updateControls()
        # self.updateInfoText()
        # self.updateTree()
        self.runValidatorsCb()
        self.runFixersCb()
        self.runReportersCb()

        maya.cmds.showWindow(self.__window)


def gui():
    ui = MayaUI()
    return ui.gui()


