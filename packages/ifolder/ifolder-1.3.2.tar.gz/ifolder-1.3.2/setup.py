from setuptools import setup, find_packages

import time
import json


def _version(V = None):
    if V:
        ver = {
            'version':V,
            'public time':time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time())), }
        json_ver = json.dumps(ver).encode('utf-8')
        with open('__version__','wb') as f:
            f.write(json_ver)
        return '.'.join(map(str, V))
    else:
        with open('__version__','rb') as f:
            json_v = f.readline().decode('utf-8')        
        ver = json.loads(json_v)
        ver['version'][2] += 1
        json_ver = json.dumps(ver).encode('utf-8')
        with open('__version__.txt','wb') as f:
            f.write(json_ver)
        
        return '.'.join(map(str, ver['version']))




setup(
    name='ifolder',
    version=_version(),
    description=(
        'ifolder is a python package for transferring files and folders with tcp socket'
    ),
    long_description=open('README.rst').read(),
    author='vinct',
    author_email='vt.y@qq.com',
    maintainer='vt',
    maintainer_email='vt.y@qq.com',
    license='MIT License',
    install_requires=[
        'tqdm',

          ],
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/vincent770/ifolder.git',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)

'''

rm -rf dist ifolder.egg-info build 
python3 setup.py sdist build
twine upload dist/*
rm -rf dist ifolder.egg-info build  

'''