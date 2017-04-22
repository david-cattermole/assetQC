"""
Validates camera instances.
"""

import assetQC.api.validator as validator


class CameraKeyframeCountValidator(validator.Validator):
    enable = True
    priority = 1
    assetTypes = ['camera']
    hostApps = ['standard']
    fixers = []

    def condition(self, ctx):
        return True

    def run(self, context):
        assert self.getInstance()
        instance = self.getInstance()
        self.assertEqual(instance.getAssetType(), 'camera')

        # shape = instance.data['shape']
        # transform = instance.data['transform']
        #
        # msg = 'No keyframes on camera.'
        # transformCount = maya.cmds.keyframe(transform, query=True, keyframeCount=True)
        # shapeCount = maya.cmds.keyframe(shape, query=True, keyframeCount=True)
        #
        # self.assertTrue(transformCount or shapeCount, msg=msg)
        return

