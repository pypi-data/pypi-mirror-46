import os
import sys

import subprocess


def load_tests(loader, standard_tests, pattern):
    # Change directory into "testing" and build the C extension module.
    os.chdir('testing')
    subprocess.run(
        [sys.executable, 'setup.py', '-q', 'build_ext', '--inplace'],
        check=True)
    # Delegate to testing/testcases.py for tests.
    sys.path.insert(1, os.getcwd())
    return loader.loadTestsFromName('testcases')
