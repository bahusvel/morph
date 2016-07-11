#!/usr/bin/env python

from setuptools import setup

setup(
	name='morph',
	version='1.0',
	description='Morph - customizable syntax meta programming language',
	author='Denis Lavrov',
	author_email='bahus.vel@gmail.com',
	url='https://github.com/bahusvel/morph',
	modules=['rules', 'compiler'],
	provides=['morph'],
	keywords=['meta', 'metaprogramming'],
	install_requires=['Click'],
	entry_points='''
        [console_scripts]
        morph=compiler:morph
    ''',
)