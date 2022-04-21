#!/usr/bin/env python

# Copyright 2015 OpenMarket Ltd
# Copyright 2018 New Vector Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup
from codecs import open
import os

here = os.path.abspath(os.path.dirname(__file__))


def read_file(path_segments):
    """Read a UTF-8 file from the package. Takes a list of strings to join to
    make the path"""
    file_path = os.path.join(here, *path_segments)
    with open(file_path, encoding="utf-8") as f:
        return f.read()


def exec_file(path_segments, name):
    """Extract a constant from a python file by looking for a line defining
    the constant and executing it."""
    result = {}
    code = read_file(path_segments)
    lines = [line for line in code.split("\n") if line.startswith(name)]
    exec("\n".join(lines), result)
    return result[name]


setup(
    name="canonicaljson",
    version=exec_file(("canonicaljson.py",), "__version__"),
    py_modules=["canonicaljson"],
    description="Canonical JSON",
    install_requires=[
        # simplerjson versions before 3.14.0 had a bug with some characters
        # (e.g. \u2028) if ensure_ascii was set to false.
        "simplejson>=3.14.0",
        # typing.Protocol was only added to the stdlib in Python 3.8
        "typing_extensions>=4.0.0; python_version < '3.8'",
    ],
    extras_require={
        # frozendict support can be enabled using the `canonicaljson[frozendict]` syntax
        "frozendict": ["frozendict>=1.0"],
    },
    zip_safe=True,
    long_description=read_file(("README.rst",)),
    keywords="json",
    author="The Matrix.org Team",
    author_email="team@matrix.org",
    url="https://github.com/matrix-org/python-canonicaljson",
    license="Apache License, Version 2.0",
    python_requires="~=3.7",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
)
