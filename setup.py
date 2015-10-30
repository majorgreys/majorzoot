#!/usr/bin/env python
from setuptools import setup

setup(name='majorzoot',
      version='0.1',
      author='Tahir Butt',
      author_email='tahir.butt@gmail.com',
      py_modules=['repo'],
      include_package_data=True,
      install_requires=[
          'click',
          'pyzotero'],
      entry_points='''
        [console_scripts]
        majorzoot=majorzoot:cli
      ''',
      )
