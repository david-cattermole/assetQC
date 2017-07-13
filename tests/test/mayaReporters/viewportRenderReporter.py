"""
Example tool for playblasting with 3D motion blur in Maya and compositing with OIIO.
"""

import os
import pprint
import subprocess
import maya.cmds
import assetQC.api.register as register
import assetQC.api.baseDataObject as baseDataObject
import assetQC.api.assetInstance as assetInstance
import assetQC.api.reporter as reporter
import assetQC.api.context as context
import assetQC.api.config as config
import assetQC.api.utils as utils

MOTION_BLUR_MODE_OFF = 'off'
MOTION_BLUR_MODE_2D = '2d'
MOTION_BLUR_MODE_3D = '3d'
MOTION_BLUR_MODE_DEFAULT = MOTION_BLUR_MODE_3D
MOTION_BLUR_MODE_LIST = [
    MOTION_BLUR_MODE_OFF,
    MOTION_BLUR_MODE_2D,
    MOTION_BLUR_MODE_3D,
]


def checkPID(pid):
    """
    Check For the existence of a unix pid.
    """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True


def getRenderImagePath(imageNumber, camera):
    fullPath = None
    if maya.cmds.about(batch=True):
        fullPath = maya.cmds.renderSettings(fullPath=True,
                                            camera=camera,
                                            genericFrameImageName=imageNumber)
    else:
        fullPath = maya.cmds.renderSettings(fullPathTemp=True,
                                            camera=camera,
                                            genericFrameImageName=imageNumber)
    if fullPath:
        fullPath = fullPath[0]
    else:
        fullPath = None
    return fullPath


class ViewportRenderReporter(reporter.Reporter):
    enable = False
    priority = 4
    assetTypes = [utils.ASSET_TYPE_ALL]
    hostApps = [utils.HOST_APP_MAYA]

    def __init__(self):
        super(self.__class__, self).__init__()
        self.__motionBlurMode = MOTION_BLUR_MODE_DEFAULT
        self.__motionBlurSamples = 3
        self.__imageFormat = 'tga'
        self.__filePath = os.path.join(config.getTempDir(), 'assetQC_<Scene>_<Camera>')
        return

    def getMotionBlurMode(self):
        return self.__motionBlurMode

    # def setMotionBlurMode(self, value):
    #     assert value in MOTION_BLUR_MODE_LIST
    #     self.__motionBlurMode = value

    def getMotionBlurSamples(self):
        return self.__motionBlurSamples

    # def setMotionBlurSamples(self, value):
    #     assert isinstance(value, int)
    #     self.__motionBlurSamples = value

    def getCameras(self):
        tmp = maya.cmds.ls(cameras=True, long=True)
        cameras = []
        for camera in tmp:
            if maya.cmds.getAttr(camera + '.renderable'):
                cameras.append(camera)
        return cameras

    def getFormat(self):
        return self.__imageFormat

    # def setFormat(self, value):
    #     assert isinstance(value, str)
    #     self.__imageFormat = value

    def run(self, ctx):
        # TODO: Add 'getters/setters' for all the other parameters
        width = 1920
        height = 1080
        startframe = int(maya.cmds.playbackOptions(query=True, minTime=True))
        endframe = int(maya.cmds.playbackOptions(query=True, maxTime=True))
        # renderer = 'mayaHardware2'
        format = self.getFormat()
        extStr = 's{sample}.{format}'
        cameras = self.getCameras()  # '|renderCamera'
        samplesNum = self.getMotionBlurSamples()  # 5  # 3
        shutterAngle = 0.5  # 180.0 / 360.0

        motionBlur = False
        motionBlurShutter = shutterAngle
        if self.getMotionBlurMode() != MOTION_BLUR_MODE_OFF:
            motionBlur = True
            if self.getMotionBlurMode() == MOTION_BLUR_MODE_2D:
                motionBlurShutter = shutterAngle
                samplesNum = 1
            elif self.getMotionBlurMode() == MOTION_BLUR_MODE_3D:
                motionBlur = False
                motionBlurShutter = shutterAngle / samplesNum

        maya.cmds.setAttr('defaultResolution.width', width)
        maya.cmds.setAttr('defaultResolution.height', height)

        maya.cmds.setAttr('defaultRenderGlobals.animation', 1)
        maya.cmds.setAttr('defaultRenderGlobals.animationRange', 0)
        maya.cmds.setAttr('defaultRenderGlobals.startFrame', startframe)
        maya.cmds.setAttr('defaultRenderGlobals.endFrame', endframe)
        maya.cmds.setAttr('defaultRenderGlobals.extensionPadding', 4)
        maya.cmds.setAttr('defaultRenderGlobals.periodInExt', 1)
        maya.cmds.setAttr('defaultRenderGlobals.useMayaFileName', 0)
        maya.cmds.setAttr('defaultRenderGlobals.putFrameBeforeExt', 1)
        # maya.cmds.setAttr('defaultRenderGlobals.currentRenderer',
        #                   renderer, type='string')
        maya.cmds.setAttr('defaultRenderGlobals.imageFilePrefix',
                          self.__filePath, type='string')

        # file extension
        if self.getMotionBlurMode() == MOTION_BLUR_MODE_3D:
            maya.cmds.setAttr('defaultRenderGlobals.outFormatControl', 2)
            maya.cmds.setAttr('defaultRenderGlobals.outFormatExt',
                              extStr.format(sample='sample', format=format),
                              type='string')
        else:
            maya.cmds.setAttr('defaultRenderGlobals.outFormatControl', 0)

        maya.cmds.setAttr('hardwareRenderGlobals.numberOfSamples', 5)
        maya.cmds.setAttr('hardwareRenderGlobals.enableMotionBlur', 1)
        maya.cmds.setAttr('hardwareRenderGlobals.motionBlurByFrame', 0.5)
        maya.cmds.setAttr('hardwareRenderGlobals.numberOfExposures', 8)

        maya.cmds.setAttr('defaultHardwareRenderGlobals.extension', 4)
        maya.cmds.setAttr('defaultHardwareRenderGlobals.multiPassRendering', 1)
        maya.cmds.setAttr('defaultHardwareRenderGlobals.renderPasses', 5)
        maya.cmds.setAttr('defaultHardwareRenderGlobals.motionBlur', 0.5)
        maya.cmds.setAttr('defaultHardwareRenderGlobals.lineSmoothing', 1)
        if format == 'exr':
            # EXR file, 16-bit EXR, B44
            maya.cmds.setAttr('defaultRenderGlobals.imageFormat', 40)
            maya.cmds.setAttr('defaultRenderGlobals.exrPixelType', 1)
            maya.cmds.setAttr('defaultRenderGlobals.exrCompression', 6)
        elif format == 'tga':
            # TGA file
            maya.cmds.setAttr('defaultRenderGlobals.imageFormat', 19)
            maya.cmds.setAttr('defaultHardwareRenderGlobals.imageFormat', 19)
        elif format == 'png':
            # PNG file
            maya.cmds.setAttr('defaultRenderGlobals.imageFormat', 32)
            maya.cmds.setAttr('defaultHardwareRenderGlobals.imageFormat', 32)

        # OGS Renderer (viewport 2.0)
        node = 'hardwareRenderingGlobals'
        maya.cmds.setAttr(node + '.multiSampleEnable', 1)  # Anti-Aliasing
        maya.cmds.setAttr(node + '.ssaoEnable', 1)  # Ambient Occlusion

        # Motion blur
        maya.cmds.setAttr(node + '.motionBlurEnable', motionBlur)
        maya.cmds.setAttr(node + '.motionBlurShutterOpenFraction',
                          motionBlurShutter)
        maya.cmds.setAttr(node + '.motionBlurSampleCount', 4)

        # TODO: Don't hard code these values.
        samplesList = [0.0]
        if samplesNum == 3:
            samplesList = [-(shutterAngle * 0.5),
                           0.0,
                           (shutterAngle * 0.5)]
        elif samplesNum == 5:
            samplesList = [-(shutterAngle * 0.5),
                           -(shutterAngle * 0.25),
                           0.0,
                           (shutterAngle * 0.25),
                           (shutterAngle * 0.5)]
        elif samplesNum == 9:
            samplesList = [-(shutterAngle * 0.5),
                           -(shutterAngle * 0.375),
                           -(shutterAngle * 0.25),
                           -(shutterAngle * 0.125),
                           0.0,
                           (shutterAngle * 0.125),
                           (shutterAngle * 0.25),
                           (shutterAngle * 0.375),
                           (shutterAngle * 0.5)]

        # save state
        # TODO: Store and restore all changed attributes.
        # maya.cmds.ogs(reset=True)  # reset internal viewport 2 database
        now = maya.cmds.currentTime(q=True)

        # pre-compute output file names and initialize data structure
        times = xrange(startframe, endframe+1)
        outputImages = {}
        sampleImages = {}
        for camera in cameras:
            sampleImages[camera] = {}
            for time in times:
                sampleImages[camera][time] = []

            maya.cmds.setAttr('defaultRenderGlobals.outFormatExt', format,
                              type='string')
            value = maya.cmds.getAttr('defaultRenderGlobals.outFormatControl')
            maya.cmds.setAttr('defaultRenderGlobals.outFormatControl', 0)
            cameraName = camera.split('|')[-1]
            tmp = getRenderImagePath('{frame}', cameraName)
            dirPath, fileName = os.path.split(tmp)
            outputImages[camera] = fileName
            maya.cmds.setAttr('defaultRenderGlobals.outFormatControl', value)

        # render
        blendProcesses = []
        for x in times:
            samples = []
            for sample in samplesList:
                samples.append(float(x) + sample)
            average = (1.0 / float(len(samples)))
            frameNum = str(x).zfill(4)

            # Render multiple sub-frames
            for i, f in enumerate(samples):
                maya.cmds.setAttr('defaultRenderGlobals.outFormatExt',
                                  extStr.format(sample=i, format=format),
                                  type='string')

                maya.cmds.currentTime(f)
                for camera in cameras:
                    maya.cmds.ogsRender(
                        noRenderView=True,
                        camera=camera,
                        enableFloatingPointRenderTarget=False,
                        enableMultisample=True,
                        frame=f, w=width, h=height)
                    sampleImage = getRenderImagePath(x, camera)
                    sampleImages[camera][x].append(sampleImage)

            # blend all the seperate samples together
            for camera in cameras:
                if len(sampleImages[camera]) > 1:
                    # run OIIO Tool to blend sub-frames together.
                    outputImage = outputImages[camera].format(frame=frameNum)
                    imagePath = sampleImages[camera][x][0]
                    imageDir = os.path.dirname(imagePath)
                    outputImage = os.path.join(imageDir, outputImage)
                    outputImage = os.path.abspath(outputImage)
                    print 'outputImage', outputImage

                    args = ['oiiotool', '-q', '--threads', '1']
                    for sampleImage in sampleImages[camera][x]:
                        args.append(sampleImage)
                        args.append('--add')

                    args.append('--cmul')
                    args.append(str(average))
                    args.append('-o')
                    args.append(outputImage)
                    p = subprocess.Popen(args)
                    blendProcesses.append(p)

        # restore state
        maya.cmds.currentTime(now)
        # maya.cmds.ogs(reset=True)  # reset internal viewport 2 database
        maya.cmds.setAttr('defaultRenderGlobals.outFormatControl', 0)

        # ensure all blend processes have completed before returning.
        for process in blendProcesses:
            pid = process.pid
            print 'process.pid', pid
            if checkPID(pid):
                try:
                    os.waitpid(pid, 0)
                except:
                    print 'Failed to wait for process PID:', pid

        # delete sample images.
        for camera in sampleImages:
            for time in sampleImages[camera]:
                for sampleImage in sampleImages[camera][time]:
                    print 'Delete', sampleImage
                    try:
                        os.remove(sampleImage)
                    except:
                        print 'Delete failed!'
                        pass

        return


manager = register.getPluginManager()
manager.registerPlugin(ViewportRenderReporter)
