#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

requirements = [
    'ibllib'
]

setup(
    name='pybpod-gui-plugin-alyx',
    version="1.1.1",
    description="""PyBpod Alyx API connection module""",
    author=['Sergio Copeto', 'Luís Teixeira'],
    author_email='sergio.copeto@research.fchampalimaud.org, ricardo.ribeiro@research.fchampalimaud.org, micboucinha@gmail.com',
    license='Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>',
    url='',

    include_package_data=True,
    packages=find_packages(),

    package_data={'pybpod_alyx_module': ['resources/*.*', ]},

    install_requires=requirements,
)
