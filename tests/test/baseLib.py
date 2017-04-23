"""
Base class for test cases.
"""

import os
import shutil
import unittest


class BaseCase(unittest.TestCase):
    def setUp(self):
        root = self.rootPath()
        if not os.path.isdir(root):
            os.makedirs(root)
        return

    def tearDown(self):
        root = self.rootPath()
        if os.path.isdir(root):
            shutil.rmtree(root)
            # print 'Removing root directory:', root
            # for base, dirs, files in os.walk(root, topdown=False):
            #     for name in files:
            #         path = os.path.join(base, name)
            #         print '-> (f)', path
            #         os.remove(path)
            #     for name in dirs:
            #         path = os.path.join(base, name)
            #         print '-> (d)', path
            #         os.rmdir(path)
            # os.removedirs(root)
        return

    def rootPath(self):
        return '/tmp/assetQC'
