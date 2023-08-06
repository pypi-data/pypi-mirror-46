from setuptools import setup, Extension


setup(
    name='testpackage',
    py_modules=['testmodule', 'srconlymodule'],
    ext_modules=[Extension('testmodule', ['testmodule.c'], optional=True)],
    test_suite='testcases',
    )
