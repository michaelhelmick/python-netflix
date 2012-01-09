#!/usr/bin/env python

import sys, os
from setuptools import setup
from setuptools import find_packages

__author__ = 'Mike Helmick <mikehelmick@me.com>'
__version__ = '1.0'

setup(
    name='python-netflix',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=['httplib2', 'oauth2', 'simplejson'],
    author='Mike Helmick',
    author_email='mikehelmick@me.com',
    license='MIT License',
    url='http://github.com/michaelhelmick/python-netflix/',
    keywords='python netflix oauth api',
    description='A Python Library to interface with Netflix REST API & OAuth',
    long_description=open('README.md').read(),
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Communications :: Chat',
        'Topic :: Internet'
    ]
)