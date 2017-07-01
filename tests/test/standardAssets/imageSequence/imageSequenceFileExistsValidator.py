"""
Validates imageSequence instances.
"""

import assetQC.api.register as register
import assetQC.api.validator as validator
import test.standardAssets.imageSequence.imageSequenceFilmbackFixer as imageSequenceFilmbackFixer


class ImageSequenceShapeValidator(validator.Validator):
    enable = True
    priority = 1
    assetTypes = ['imageSequence']
    hostApps = ['standalone']
    fixers = []

    def condition(self, ctx):
        return True

    def run(self, context):
        assert self.getInstance()
        instance = self.getInstance()
        self.assertEqual(instance.getAssetType(), 'imageSequence')

        imagePath = instance.getDirPath()
        self.assertTrue(os.path.isdir())
        return

manager = register.getPluginManager()
manager.registerPlugin(ImageSequenceFilmbackValidator)
