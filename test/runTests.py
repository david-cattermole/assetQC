"""
Sets up and runs tests for the 'assetQC' API.

To be run with:
$ env ASSETQC_CONFIG_PATH='/home/davidc/dev/mayaScripts/trunk/assetQC/test/config/config.json' python runTests.py
"""

import sys
import os
import unittest

# Ensure that '<root>/python' and '<root>/test' is on the PYTHONPATH
path = os.path.dirname(__file__)
test_path = os.path.abspath(os.path.join(path, '..'))
package_path = os.path.abspath(os.path.join(path, '..', 'python'))
sys.path.append(path)
sys.path.append(package_path)


import test.baseLib
import test.standardUtils as stdUtils
import assetQC.api.config as config
import assetQC.api.lib as lib
import assetQC.api.context as context


class TestOverall(test.baseLib.BaseCase):
    def test_one(self):
        stdUtils.createCameraAsset(name='renderCam')

        # do checks
        ctx = context.Context(find=context.FIND_MODE_ALL)
        lib.run(ctx=ctx)
        return


# if __name__ == '__main__':
#     import coverage
#     import nose
#
#     cov = None
#     ver = str(coverage.__version__).split('.')
#     msg = 'version:' + repr(ver)
#     print msg
#     if int(ver[0]) == 3:
#         cov = coverage.coverage()
#         cov.exclude('*python*site-packages*')
#     elif int(ver[0]) >= 4:
#         cov = coverage.Coverage(omit='*test*')
#     else:
#         pass
#     cov.erase()
#     cov.start()
#
#     nose.core.run()
#     # (suite=AssetQCTestSuite())
#
#     cov.stop()
#     cov.save()
#     cov.report()
#     # cov.html_report()
