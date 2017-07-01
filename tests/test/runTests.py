"""
Sets up and runs tests for the 'assetQC' API.

To be run with:
$ env ASSETQC_CONFIG_PATH='/home/davidc/dev/mayaScripts/trunk/assetQC/test/config/config.json' python runTests.py
"""

import os
import sys

# Ensure that '<root>/python' and '<root>/tests' is on the PYTHONPATH
path = os.path.dirname(__file__)
test_path = os.path.abspath(os.path.join(path, '..'))
package_path = os.path.abspath(os.path.join(path, '../..', 'python'))
sys.path.insert(0, test_path)
sys.path.insert(0, package_path)


if __name__ == '__main__':
    exe = sys.executable
    exe_path = None
    exe_name = None
    if exe:
        exe_path, exe_name = os.path.split(exe)
    if exe_name == 'python-bin' and 'maya' in exe_path:
        import runMayaTests
        import maya.cmds
        runMayaTests.main()
        maya.cmds.quit()
    else:
        import coverage
        import nose

        cov = None
        ver = str(coverage.__version__).split('.')
        msg = 'version:' + repr(ver)
        print msg
        if int(ver[0]) == 3:
            cov = coverage.coverage()
            cov.exclude('*python*site-packages*')
        elif int(ver[0]) >= 4:
            cov = coverage.Coverage(omit='*test*')
        else:
            pass
        cov.erase()
        cov.start()

        nose.core.run()

        cov.stop()
        cov.save()
        cov.report()
        cov.html_report()

