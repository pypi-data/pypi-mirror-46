# Add the dualtest package directory to the path so that
# dualtest can be used here.
import sys
import os.path

directory = os.path.dirname(__file__)
# Go up a level
directory = os.path.dirname(directory)
sys.path.insert(1, directory)
del directory
# In other projects you would use the "tests_require" feature from setuptools
# to make dualtest available.

from importlib.machinery import SourceFileLoader

from dualtest import DualTestCase


class ModuleImportTestCase(DualTestCase):
    # List of modules to import, they will be added to the module globals when
    # the tests are run.
    import_names = ['testmodule']

    def test_module_import(self):
        'Test if the module was imported and added as a global'
        module = globals().get('testmodule')
        self.assertIsNotNone(module, 'testmodule global')


# If the Python version of the module can't be imported, it will be an error.
# If the C version of the module can't be imported,
# the test case will be skipped.
class SkippedExtensionImportTestCase(DualTestCase):
    import_names = ['srconlymodule']

    def test_nonexisting_extension(self):
        'This test is expected to be skipped for extensions.'
        if not ('srconlymodule' in globals()
                and isinstance(srconlymodule.__loader__, SourceFileLoader)):
            self.fail('Extension test was not skipped')


class ModuleImportFromTestCase(DualTestCase):
    # Attributes to import from modules.
    import_from_names = [
        ('testmodule', ['testmethod']),
        ]

    def test_import_from(self):
        'Test if the imported name was added as a global'
        method = globals().get('testmethod')
        self.assertIsNotNone(method, 'testmethod global')


class ModuleImportAllFromTestCase(DualTestCase):
    # Using "*" as the name to import causes all public names to be imported.
    import_from_names = [
        ('testmodule', ['*']),
        ]

    def test_import_from(self):
        'Test if the imported name was added as a global'
        method = globals().get('testmethod')
        self.assertIsNotNone(method, 'testmethod global')
