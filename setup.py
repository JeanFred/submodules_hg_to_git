#!/usr/bin/python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

py_modules = ['submodules_hg_to_git']
requires = []
scripts = []
setup(
    name='submodules_hg_to_git',
    version='0.1',
    author='Jean-Frédéric',
    author_email='JeanFred@github',
    url='',
    description='Converting the submodules from a hg repo to a git repo.',
    license='MIT',
    py_modules=py_modules,
    install_requires=requires,
    scripts=scripts,
)
