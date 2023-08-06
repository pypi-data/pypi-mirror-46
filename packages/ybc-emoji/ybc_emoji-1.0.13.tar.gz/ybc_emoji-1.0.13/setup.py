#!/usr/bin/env python

from distutils.core import setup

setup(name='ybc_emoji',
      version='1.0.13',
      description='Generateing image using emoji.',
      long_description='Generateing image using emoji.',
      author='hurs',
      author_email='hurs@fenbi.com',
      keywords=['pip3', 'ybc_emoji', 'python3','python','emoji'],
      url='http://pip.zhenguanyu.com/',
      packages = ['ybc_emoji'],
      package_data={'ybc_emoji': ['__init__.py', 'ybc_echarts.py', 'ybc_echarts_unitest.py']},
      license='MIT',
      install_requires=['ybc_exception', 'pillow']
      )
