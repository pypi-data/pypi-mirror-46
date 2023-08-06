#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import re, os
from pyqo import __version__
from pyqo import __author__
from pyqo import __email__

PYQ_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),'pyqo')

#commands
def commands():
    files = os.listdir(PYQ_PATH)
    pattern = re.compile("^[^_].*.py$")
    commands = [file[:-3] for file in files if pattern.match(file)]
    return commands

COMMANDS = commands()
CONSOLE_SCRIPTS = ['{c}=pyqo.{c}:main'.format(c=command) for command in COMMANDS]
SCRIPTS = ['bin/c','bin/c.bat']

#requirements
def requirements():
    with open('requirements.txt','r',encoding = 'utf-8') as f:
        lines = f.readlines()
        return [line.replace('==','>=').strip() for line in lines]
REQUIREMENTS = requirements()

#readme
with open('README.md', 'r', encoding = 'utf-8') as f:
    README = '\n'.join(f.readlines())

#setup
setup(
    name='pyqo',
    version=__version__,
    description='Useful collection of command line scripts.',
    long_description_content_type='text/markdown',
    long_description=README,
    author=__author__,
    author_email=__email__,
    url='https://github.com/Whenti/pyqo',
    packages = ['pyqo'],
    package_dir={'pyqo':'pyqo'},
    include_package_data=True,
    install_requires=REQUIREMENTS,
    license='Apache License',
    zip_safe=False,
    keywords='command line scripts',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    scripts = SCRIPTS,
    entry_points={
        'console_scripts': CONSOLE_SCRIPTS,
    },
)
