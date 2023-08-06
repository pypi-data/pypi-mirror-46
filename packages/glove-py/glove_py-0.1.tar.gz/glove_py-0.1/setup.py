#!/usr/bin/env python

# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import sys
import setuptools
import os
import subprocess
import platform

__version__ = '0.1'
SRC = "src"


# Based on https://github.com/pybind/python_example

class get_pybind_include(object):
    """Helper class to determine the pybind11 include path

    The purpose of this class is to postpone importing pybind11
    until it is actually installed, so that the ``get_include()``
    method can be invoked. """

    def __init__(self, user=False):
        try:
            import pybind11
        except ImportError:
            if subprocess.call([sys.executable, '-m', 'pip', 'install', 'pybind11']):
                raise RuntimeError('pybind11 install failed.')

        self.user = user

    def __str__(self):
        import pybind11
        return pybind11.get_include(self.user)


try:
    coverage_index = sys.argv.index('--coverage')
except ValueError:
    coverage = False
else:
    del sys.argv[coverage_index]
    coverage = True

src_files = map(str, os.listdir(SRC))
src_cpp = list(filter(lambda x: x.endswith('.cpp'), src_files))

src_cpp = list(
    map(lambda x: str(os.path.join(SRC, x)), src_cpp)
)

print(get_pybind_include())
print(get_pybind_include(user=True))
src_cpp.append('python/glove/pybind/glove_pybind.cpp')
print(src_cpp)
ext_modules = [
    Extension(
        "glove_pybind",
        # Path to pybind11 headers
        src_cpp,
        include_dirs=[
            get_pybind_include(),
            get_pybind_include(user=True),
            # Path to fasttext source code
            SRC,
        ],
        language='c++',
        extra_compile_args=["-std=c++11"],
    ),
]


def _get_readme():
    """
    Use pandoc to generate rst from md.
    pandoc --from=markdown --to=rst --output=python/README.rst python/README.md
    """
    with open("python/README.rst") as fid:
        return fid.read()


setup(
    name='glove_py',
    version=__version__,
    author='Wang Heng',
    author_email='me@lightgoing.com',
    description='glove Python bindings',
    ext_modules=ext_modules,
    url='https://github.com/facebookresearch/fastText',
    license='MIT',
    # classifiers=[ 'Programming Language :: Python :: 3', ],
    install_requires=['pybind11>=2.2', "setuptools >= 0.7.0", "numpy"],
    # cmdclass={'build_ext': BuildExt},
    packages=["glove", "glove.pybind", ],
    package_dir={'': 'python'},
    zip_safe=False,
)
