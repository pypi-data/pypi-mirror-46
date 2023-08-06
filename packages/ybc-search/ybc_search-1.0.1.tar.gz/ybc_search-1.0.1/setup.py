#!/usr/bin/env python

from distutils.core import setup

setup(name='ybc_search',
      version='1.0.1',
      description='Search Article or Picture.',
      long_description='Search Article or Picture.',
      author='mengxf01',
      author_email='mengxf01@fenbi.com',
      keywords=['python', 'object', 'search', 'article', 'picture'],
      url='http://pip.zhenguanyu.com/',
      packages=['ybc_search'],
      package_data={'ybc_search': ['*.py']},
      license='MIT',
      install_requires=['ybc_exception', 'ybc_config']
      )