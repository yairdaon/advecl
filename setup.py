try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'solveing advection equation using open Cl',
    'author': 'Yair Daon',
    'url': 'https://github.com/yairdaon/advecl',
    'download_url': 'https://github.com/yairdaon/advecl',
    'author_email': 'yair.daon@gmail.com',
    'version': '1.0',
    'install_requires': ['nose'],
    'packages': ['advecl'],
    'scripts': [],
    'name': 'advecl'
}

from distutils.core import setup, Extension
import numpy.distutils.misc_util

setup(
    ext_modules=[Extension("_aux", ["_advecl.c", "advecl.c"])],
    include_dirs=numpy.distutils.misc_util.get_numpy_include_dirs(),
)

setup(**config)
