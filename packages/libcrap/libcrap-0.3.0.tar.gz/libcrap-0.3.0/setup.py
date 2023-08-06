#!/usr/bin/env python

from setuptools import setup


setup(
    name='libcrap',
    version='0.3.0',
    description='Crappy functions Crabman uses. Some helpers for pytorch and ignite.',
    author='Philip Blagoveschensky',
    author_email='me@crabman.me',
    url='https://bitbucket.org/nemelex/libcrap',
    packages=['libcrap'],
    license='MIT',
    install_requires=[
        'tqdm>=4.8.4',
        'typing>=3.5.2.2',
        'more-itertools>=7.0.0'],
    extras_require={
        'torch': ['torch>=1.0.1'],
        'ignite_train': ['pytorch-ignite>=0.2.0'],
        'test': ['pytest>=3.0.4']
    },
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 2 - Pre-Alpha',
        'Topic :: Software Development :: Libraries :: Python Modules'])
