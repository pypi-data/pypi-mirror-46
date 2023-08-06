#!/usr/bin/env python

from distutils.core import setup

setup(name='ybc_coordinate',
      version='1.0.6',
      description='City coordinate.',
      long_description='City coordinate.',
      author='hurs',
      author_email='hurs@fenbi.com',
      keywords=['python', 'city', 'coordinate'],
      url='http://pip.zhenguanyu.com/',
      packages=['ybc_coordinate'],
      package_data={'ybc_coordinate': ['*.py']},
      license='MIT',
      install_requires=['ybc_exception']
     )