"""
Validates rig instances.
"""

import maya.cmds
import assetQC.api.validator as validator


class RigValidator(validator.Validator):
    enable = True
    priority = 1
    assetTypes = ['rig']
    hostApps = ['maya']
    fixers = []

    def condition(self, ctx):
        return True

    def run(self, context):
        instance = self.getInstance()
        assert instance

        keyword = 'rig_set'
        msg = 'Rig Set cannot be found, {0!r}'
        msg = msg.format(instance.data)
        self.assertTrue(keyword in instance.data, msg=msg)

        rigSet = instance.data[keyword]
        msg = 'Rig Set node does not exist. {0!r}'
        msg = msg.format(instance.data)
        self.assertTrue(maya.cmds.objExists(rigSet), msg=msg)

        keyword = 'ctrl_set'
        msg = 'Control Set cannot be found, {0!r}'
        msg = msg.format(instance.data)
        self.assertTrue(keyword in instance.data, msg=msg)

        rigSet = instance.data[keyword]
        msg = 'Control Set node does not exist. {0!r}'
        msg = msg.format(instance.data)
        self.assertTrue(maya.cmds.objExists(rigSet), msg=msg)
        return
