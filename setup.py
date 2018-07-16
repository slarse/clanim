# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

test_requirements = [
    'pytest>=3.1.1', 'pytest-cov>=2.5.1', 'codecov', 'asynctest'
]
required = ['clanimtk']

setup(
    name='clanim',
    version='0.3.0',
    description='Command line animations built with clanimtk.',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Simon Larsén',
    author_email='slarse@kth.se',
    url='https://github.com/slarse/clanim',
    download_url='https://github.com/slarse/clanim/archive/v0.3.0.tar.gz',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    tests_require=test_requirements,
    install_requires=required,
    include_package_data=True,
    zip_safe=False)
