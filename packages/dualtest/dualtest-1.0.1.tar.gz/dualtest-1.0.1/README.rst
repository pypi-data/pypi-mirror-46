When you write a C extension, you can provide a Python version as a backup. A
problem with this is that only one of these modules will be tested, while the
other is neglected.

DualTest provides a class that, when inherited from, imports a list of modules
and attributes from modules and makes them available as globals during tests.
Allowing you to easily test both versions of a module and write just one set of
tests.

=====
Usage
=====

Create a test case class derived from DualTestCase and set the `import_names`
or `import_from_names` class attributes.

`import_names` should be set to a list of the names of modules with Python
source and C extension versions to import:

.. code:: python

    class ImportTestCase(DualTestCase):
        import_names = ['mod1', 'mod2']

        def test_something(self):
            # mod1 and mod2 will be available here.

`import_from_names` causes attributes to be imported from modules just like
`from module import attribute` would. It should be set to a list of tuples
containing the name of the module to import from, and a list of attribute names
to import. If one of the attribute names is "*", then all public attributes are
imported:

.. code:: python

    class ImportFromTestCase(DualTestCase):
        import_from_names = [
            ('mod1', ['attr1', 'attr2']),
            # "*" causes all public attributes to be imported.
            ('mod2', ['*']),
            ]

        def test_something(self):
            # attr1, attr2 and everything from mod2 will be available here.

============
Full Example
============

.. code:: python

    from dualtest import DualTestCase


    class ImportTestCase(DualTestCase):
        import_names = ['mod1', 'mod2']

        def test_something(self):
            # mod1 and mod2 will be available here.


    class ImportFromTestCase(DualTestCase):
        import_from_names = [
            ('mod1', ['attr1', 'attr2']),
            # "*" causes all public attributes to be imported.
            ('mod2', ['*']),
            ]

        def test_something(self):
            # attr1, attr2 and everything from mod2 will be available here.

=========
Changelog
=========

1.0.1
-----

* Patch imported modules into "sys.modules" during tests.
* Fix error when "import_from_names" references a non-existing module.
* Fix bug when importing '*' from a module.
* Add module type context when "subTest" is called.
