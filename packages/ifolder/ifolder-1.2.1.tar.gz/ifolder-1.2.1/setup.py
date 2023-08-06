from setuptools import setup, find_packages

setup(
    name='ifolder',
    version='1.2.1',
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
          ],
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/vincent770/ifolder.git',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
)