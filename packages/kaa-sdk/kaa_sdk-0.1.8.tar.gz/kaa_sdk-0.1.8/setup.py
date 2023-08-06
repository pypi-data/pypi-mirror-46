#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='kaa_sdk',
      version='0.1.8',
      description='Python client for Kaa API',
      author='Alexandr Agitolyev',
      author_email='aagitolyev@kaaiot.io',
      packages=find_packages(),
      install_requires=["requests"]
      )
