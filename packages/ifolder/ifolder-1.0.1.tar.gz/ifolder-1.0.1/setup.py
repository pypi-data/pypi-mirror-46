#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='ifolder',
    version='1.0.1',
    description=(
        'ifolder is a python package for transferring files and folders with tcp socket'
    ),
    long_description=open('README.rst').read(),
    author='vinct',
    author_email='vt.y@qq.com',
    maintainer='vt',
    maintainer_email='vt.y@qq.com',
    license='MIT License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/vincent770/ifolder.git',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
)