#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
doclink = """
Documentation
-------------

The full documentation is at http://yafa_grpc.rtfd.org."""
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='yafa_grpc',
    version='0.1.0',
    description='Stock trading backtesting with grpc',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='Graham Crowell',
    author_email='graham.crowell@gmail.com',
    url='https://github.com/gcrowell/yafa_grpc',
    packages=['yafa_grpc', '.'],
    package_dir={'yafa_grpc': 'yafa_grpc'},
    include_package_data=True,
    install_requires=[],
    license='MIT',
    zip_safe=False,
    keywords='yafa_grpc',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    entry_points={
        'console_scripts': [
            'start_server=yafa_grpc.command_line:server',
            'start_client=yafa_grpc.command_line:client'
        ]
    })
