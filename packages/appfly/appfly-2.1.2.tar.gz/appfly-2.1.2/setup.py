#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'Flask==1.0.2',
    'flask_cors==3.0.6', 
    'Flask-SocketIO==3.0.2',
    'jsonmerge==1.5.2',
    'deeptracepy==0.1.0',
    'gevent==1.4.0'
]

setup(
    author="Italo José G. de Oliveira",
    author_email='italo.i@live.com',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="This pkg encapsulate the base flask server configurations",
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords='appfly',
    name='appfly',
    packages=find_packages(),
    url='https://github.com/italojs/appfly',
    version='2.1.2',
    zip_safe=False,
)
