#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""PyBeerYAML A YAML format parser for beer storage"""

# Pybeeryaml
# Copyright (C) 2018  TROUVERIE Joachim <joachim.trouverie@linoame.fr>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from setuptools import setup, find_packages
from pybeeryaml import __author__, __url__, __version__, __email__


requirements = []
for line in open('REQUIREMENTS.txt', 'r'):
    requirements.append(line)

setup(
    name="pybeeryaml",
    packages=find_packages(),
    version=__version__,
    description=__doc__,
    long_description=open('README.rst').read(),
    author=__author__,
    author_email=__email__,
    url="https://pythonhosted.org/pybeeryaml/",
    download_url=__url__,
    install_requires=requirements,
    tests_require=["pytest"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",  # noqa
        "Natural Language :: English",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Utilities",
    ],
)
