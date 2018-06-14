#!/usr/bin/env python
from distutils.core import setup

with open('README.rst', 'rb') as f:
    readme = f.read().decode('utf-8')

setup(name='vnimport',
      version='0.1',
      description='Playnite Plugin for Importing Visual Novel Metadata',
      long_description=readme,
      long_description_content_type='text/x-rst',
      author='Wiktor Duda',
      author_email='wiktorduda@protonmail.com',
      license='BSD 3-Clause License',
      platforms='Windows',
      url='https://github.com/wiktorduda/vnimport',
      packages=['vnimport']
     )