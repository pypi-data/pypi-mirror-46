#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='s3sh',
    version='0.1.5',
    description='A repl for s3',
    long_description='Traverse s3 just like it would be a filesystem',
    author='Wim Berchmans',
    author_email="wimberchmans@gmail.com",
    license='',
    url='https://github.com/WRRB/s3sh',
    include_package_data=True,
    package_data={},
    packages=find_packages(),
    install_requires=['boto3'],
    tests_require=[],
    scripts=['trail/cli/trail', 'trail/cli/trail.bat'],
    zip_safe=False
)
