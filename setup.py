# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

test_requirements = ['pytest>=3.1.1', 'pytest-cov>=2.5.1', 'codecov', 
                     'asynctest']
required = ['daiquiri']

setup(
    name='clanim',
    version='0.1.0',
    description=('Function decorators that cause a command line animation to be run for the duration of the function.'),
    long_description=readme,
    author='Simon Larsén',
    author_email='slarse@kth.se',
    url='https://github.com/slarse/clanim',
    download_url='https://github.com/slarse/clanim/archive/v0.1.0.tar.gz',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    tests_require=test_requirements,
    install_requires=required,
    scripts=['bin/clanim'],
    include_package_data=True,
    zip_safe=False
)
