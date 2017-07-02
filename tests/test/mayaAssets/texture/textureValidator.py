"""
Validates rig instances.
"""

import os

import assetQC.api.register as register
import assetQC.api.validator as validator

TEXTURE_EXTENSIONS = ['png', 'jpeg', 'jpg', 'tga', 'bmp',
                      'exr', 'tif', 'tiff', 'hdr']


class TextureValidator(validator.Validator):
    enable = True
    priority = 1
    assetTypes = ['texture']
    hostApps = ['maya']
    fixers = []

    def condition(self, ctx):
        return True

    def run(self, context):
        instance = self.getInstance()

        fileName = instance.data['fileName']
        filePath = instance.data['filePath']
        dirPath = instance.data['dirPath']
        msg = 'Invalid texture file path: %s' % repr(filePath)
        self.assertTrue(os.path.isfile(filePath), msg=msg)
        self.assertTrue(os.path.isdir(dirPath), msg=msg)
        self.assertTrue(os.path.join(dirPath, fileName) == filePath, msg=msg)
        self.assertTrue(os.path.isabs(dirPath), msg=msg)
        self.assertTrue(os.path.isabs(filePath), msg=msg)

        # ensure the image extension matches.
        fileName, fileExt = os.path.splitext(filePath)
        msg = 'Invalid texture extension: %s' % repr(fileExt)
        if fileExt.startswith('.'):
            fileExt = fileExt[1:]
        if fileExt not in TEXTURE_EXTENSIONS:
            self.assertTrue(fileExt in TEXTURE_EXTENSIONS, msg=msg)

        return

manager = register.getPluginManager()
manager.registerPlugin(TextureValidator)
