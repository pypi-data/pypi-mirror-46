from pathlib import Path
from setuptools import setup


desc = 'Easily test both Python and C versions of modules.'
readme = Path('README.rst')

setup(
    name='dualtest',
    version='1.0.1',
    description=desc,
    long_description=readme.read_text(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Testing',
        ],
    python_requires='>= 3.6',

    py_modules=['dualtest'],
    test_suite='tests',
    )
