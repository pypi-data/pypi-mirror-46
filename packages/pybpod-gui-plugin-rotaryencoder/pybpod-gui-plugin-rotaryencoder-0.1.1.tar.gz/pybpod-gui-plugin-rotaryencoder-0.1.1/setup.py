#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
	name='pybpod-gui-plugin-rotaryencoder',
	version="0.1.1",
	description="""PyBpod rotary encoder module controller""",
	author=['Ricardo Ribeiro', 'Luís Teixeira'],
	author_email='ricardojvr@gmail.com, micboucinha@gmail.com',
	license='Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>',
	url='https://bitbucket.org/fchampalimaud/rotary-encoder-module',

	include_package_data=True,
	packages=find_packages(),

	package_data={'pybpod_rotaryencoder_module': ['resources/*.*',]}
)