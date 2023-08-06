#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

requirements = [
    'libusb',
    'pyusb',
    'aenum'
]

setup(
    name='pybpod-gui-plugin-soundcard',
    version='0.1.5',
    description="""PyBpod Sound card module""",
    long_description="""Library to control the Harp Sound Card board developed by the Scientific Hardware Platform at 
    the Champalimaud Foundation.""",
    author='Luís Teixeira',
    author_email='micboucinha@gmail.com',
    license='Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>',
    url='https://bitbucket.org/fchampalimaud/pybpod-soundcard-module',

    include_package_data=True,
    packages=find_packages(),

    package_data={'pybpod_soundcard_module': ['resources/*.*',]},
    install_requires=requirements,
)
