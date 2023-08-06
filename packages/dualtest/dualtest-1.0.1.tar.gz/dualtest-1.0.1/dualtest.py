"""
Test case class that lets you test Python source and C extension versions of a
module simultaneously.

To easily use this module in your testcases, add `tests_require=['dualtest']`
to your setup call in your setup.py script.
"""
import sys

from functools import wraps
from importlib import import_module
from importlib.machinery import (
    FileFinder,
    SourceFileLoader, SOURCE_SUFFIXES,
    ExtensionFileLoader, EXTENSION_SUFFIXES
    )
from importlib.util import resolve_name, module_from_spec
from unittest import TestCase, SkipTest
from unittest.mock import patch


__all__ = ('DualTestCase',)


def iter_module_names(module):
    """
    Yields tuples for all public names in the given module.
    """
    # Try using __all__ first.
    try:
        module.__all__
    except AttributeError:
        pass
    else:
        for name in module.__all__:
            yield name, getattr(module, name)
        return

    # When there is no __all__ declaration,
    # yield every name not beginning with _
    for name, val in module.__dict__.items():
        if not name.startswith('_'):
            yield name, val


class BaseImporter:
    """
    Handles importing modules and attributes and patching them into the test
    case's globals.

    Instance attributes:
        patches: A list of patch.multiple objects for the imported modules and
                 attributes.

        exception: Exception type to raise during the test when not None.

        exc_args: Positional args and keyword args for the exception.

    Class attributes:
        module_cache: dict object for caching loaded modules.

    Derived classes need to define these:
        loader_details: Argument for FileFinder objects.

        module_not_found: Called when a module could not be loaded. Should set
                          the exception to raise.
    """
    exception = None
    exc_args = [(), {}]

    def __init_subclass__(cls, **kw):
        super().__init_subclass__(**kw)
        cls.module_cache = {}

    def __init__(self, cls):
        # dict mapping modules to modules and attributes to be patched into that
        # module. The dicts are passed to patch.multiple calls.
        # e.g.
        # {
        #   <testcasemodule>: {'mod1': <module>, 'mod2': <module>,
        #                      'attr1': <object>, 'attr2': <object>, ...},
        #   ...
        # }
        patches = {}
        # dict of modules to be patched into sys.modules with patch.dict.
        modules = {}

        for curcls in reversed(cls.mro()):
            # Reference to the test case class's module.
            destmod = import_module(curcls.__module__)
            # Patches for the test case class's globals.
            destmodpatches = patches.setdefault(destmod, {})

            # Import modules.
            for modname in curcls.__dict__.get('import_names', ()):
                # Resolve possible relative module name.
                modname = resolve_name(modname, destmod.__package__)

                module = self.import_module(modname)

                if module is None:
                    self.module_not_found(modname)
                    return
                else:
                    destmodpatches[module.__name__] = module
                    modules[module.__name__] = module

            # Import module attributes.
            for modname, namelist in curcls.__dict__.get(
                    'import_from_names', ()):
                # Resolve possible relative module name.
                modname = resolve_name(modname, destmod.__package__)

                module = self.import_module(modname)

                if module is None:
                    self.module_not_found(modname)
                    return

                modules[module.__name__] = module

                for name in namelist:
                    if name == '*':
                        # Import all public attributes.
                        for name, val in iter_module_names(module):
                            destmodpatches[name] = val
                    else:
                        try:
                            destmodpatches[name] = getattr(module, name)
                        except AttributeError:
                            args = (f"cannot import name '{name}'",)
                            self.exc_args = [args, {}]
                            self.exception = ImportError
                            return

        # Create the patches.
        module_patches = []
        # Patch for sys.modules.
        if modules:
            module_patches.append(patch.dict('sys.modules', modules))

        # Patches for imported modules and attributes.
        for destmod, destmodpatches in patches.items():
            if destmodpatches:
                import_patch = patch.multiple(destmod, create=True,
                                              **destmodpatches)
                module_patches.append(import_patch)
        self.patches = module_patches

    @classmethod
    def import_module(cls, name):
        try:
            # Check for cached module.
            return cls.module_cache[name]
        except KeyError:
            pass

        # Try to find and import the module.
        for path in sys.path:
            finder = FileFinder(path, cls.loader_details)
            spec = finder.find_spec(name)
            if spec is not None:
                module = module_from_spec(spec)
                spec.loader.exec_module(module)
                # Cache for later use.
                cls.module_cache[name] = module
                return module
        return None

    def __enter__(self):
        # Applies the patches or raises the set exception.
        if self.exception is not None:
            args, kwargs = self.exc_args
            raise self.exception(*args, **kwargs)

        for import_patch in self.patches:
            import_patch.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        for import_patch in reversed(self.patches):
            import_patch.stop()


class SourceImporter(BaseImporter):
    loader_details = (SourceFileLoader, SOURCE_SUFFIXES)

    def module_not_found(self, modname):
        # Missing Python source modules are an error.
        args = (f"No source module named '{modname}'",)
        kwargs = {'name': modname}
        self.exc_args = [args, kwargs]
        self.exception = ImportError


class ExtensionImporter(BaseImporter):
    loader_details = (ExtensionFileLoader, EXTENSION_SUFFIXES)

    def module_not_found(self, modname):
        # Missing C extension modules are skipped.
        args = (f"Extension module not available for '{modname}'",)
        self.exc_args = [args, {}]
        self.exception = SkipTest


class DualTestCase(TestCase):
    """
    Test case which imports and runs tests for both Python source and
    C extension versions of modules.

    Derived classes can specify what to import by setting the `import_names`
    and `import_from_names` class attributes:

        `import_names`, if set, should be a list of module names to import.

        `import_from_names`, if set, should be a list of tuples containing the
        name of the module to import from and a list of attributes to import.
        Example:

            class MyTestCase(DualTestCase):
                import_from_names = [
                    ('mod1', ['attr1', 'attr2']),
                    # '*' imports all public attributes.
                    ('mod2', ['*']),
                    ]

    The imported modules and attributes are made available as globals during
    tests.

    By default, DualTestCase finds tests by looking for methods starting with
    "test", You can specify an different prefix by setting the testMethodPrefix
    class attribute.

    Some private data is stored in attributes starting with "_import".
    """
    testMethodPrefix = 'test'

    def __init_subclass__(cls, **kw):
        super().__init_subclass__(**kw)

        cls._import_source = SourceImporter(cls)
        cls._import_extension = ExtensionImporter(cls)

        # Decorate test methods.
        for attrname, val in cls.__dict__.items():
            if attrname.startswith(cls.testMethodPrefix):
                testmethod = cls._import_test_decorator(val)
                setattr(cls, attrname, testmethod)

    @classmethod
    def _import_test_decorator(cls, wrapped):
        """
        Decorator for the test case's test methods that runs the test for both
        versions of imported modules.
        """
        @wraps(wrapped)
        def run_test(self, *args, **kw):
            contextlist = [
                ('Source', cls._import_source),
                ('Extension', cls._import_extension),
                ]
            for context, importer in contextlist:
                context_patch = patch.object(self, '_import_context',
                                             context, create=True)
                with context_patch, super().subTest(context), importer:
                    wrapped(self, *args, **kw)
        return run_test

    def subTest(self, *args, **params):
        # Add module type to params
        if not args:
            args = (self._import_context,)
        else:
            params.setdefault('context', self._import_context)
        return super().subTest(*args, **params)
