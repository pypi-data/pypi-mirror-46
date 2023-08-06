from setuptools import setup, find_packages

import sys
import os

def publish():
    """Publish to PyPi"""
    print('publishing...')
    os.system("rm -rf dist ifolder.egg-info build")
    os.system("python3 setup.py sdist build")
    os.system("twine upload dist/*")
    os.system("rm -rf dist ifolder.egg-info build")
    print('done successfully!')

def _VERSION(set_ver = None, increase=False):
    import time
    import json
    if set_ver:
        ver = {
            'version':set_ver,
            'published time':time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time())), }
        with open('ifolder/__version__.py','wb') as f:
            f.write(json.dumps(ver).encode('utf-8'))

        return '.'.join(map(str, set_ver))
    else:
        with open('ifolder/__version__.py','rb') as f:
            json_v = f.readline().decode('utf-8')        
        ver = json.loads(json_v)

        if increase:
            ver['version'][2] += 1
        
        with open('ifolder/__version__.py','wb') as f:
            f.write(json.dumps(ver).encode('utf-8'))
        
        return '.'.join(map(str, ver['version']))

if sys.argv[-1] == "-p":
    _VERSION(increase=True)
    publish()
    sys.exit()

setup(
    name='ifolder',
    version=_VERSION(),
    # version=_version([1,5,6]),
    description=('ifolder is a python package for transferring files and folders with tcp socket'),
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

# python3 setpu.py -p
