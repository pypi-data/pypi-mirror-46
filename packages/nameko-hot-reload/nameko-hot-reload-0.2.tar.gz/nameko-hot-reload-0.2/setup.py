#!/usr/bin/env python
# -*- coding: utf-8 -*

import os

from setuptools import find_packages, setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


with open('requirements.txt') as f:
    install_requires = f.read().splitlines()


setup(
    name='nameko-hot-reload',
    version='0.2',
    packages=find_packages('src', exclude=('tests',)),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    description='Nameko run with autoloading, logging file CLI option',
    author='Joey.Jiang',
    author_email='joeeey9303@gmail.com',
    maintainer='Joey.Jiang',
    maintainer_email='joeeey9303@gmail.com',
    license='Apache License 2.0',
    long_description=(
        'https://github.com/joeeeeey/nameko_hot_reload'
    ),
    entry_points={
        'console_scripts': [
            'nameko_hot_reload=nameko_hot_reload.cli.main:main',
        ],
    },
    install_requires=install_requires,
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP'
    ]
)
