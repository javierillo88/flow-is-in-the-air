# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import os
import subprocess
from distutils.command.build import build as _build

import setuptools


REQUIRED_PACKAGES = ['requests']

setuptools.setup(
    name='dataflow',
    version='0.0.1',
    description='Dataflow set workflow package.',
    install_requires=REQUIRED_PACKAGES,
    packages=setuptools.find_packages()
    )
