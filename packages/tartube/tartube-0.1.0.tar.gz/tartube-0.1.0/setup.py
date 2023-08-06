#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 A S Lewis
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.


"""Standard python setup file."""


# Import modules
from setuptools import setup, find_packages


# Import documents
#with open('README.rst') as f:
#    readme = f.read()

#with open('LICENSE') as f:
#    license = f.read()


# Setup
setup(
    name='tartube',
    version='0.1.000',
    description='GUI front-end for youtube-dl',
    long_description="""# Tartube""",
    long_description_content_type='text/markdown',
    author='A S Lewis',
    author_email='aslewis@cpan.org',
    url='https://github.com/axcore/tartube',
#    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

