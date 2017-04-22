"""
Base class for test cases.
"""

import os
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
            os.removedirs(root)
        return

    def rootPath(self):
        return '/tmp/assetQC'
