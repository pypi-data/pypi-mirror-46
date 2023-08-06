#!/usr/bin/env python

from distutils.core import setup

setup(name='ybc_food',
      version='1.0.18',
      description='Recognize food image.',
      long_description='To judge a food image or recognize a food image.',
      author='hurs',
      author_email='hurs@fenbi.com',
      keywords=['python', 'food', 'image'],
      url='http://pip.zhenguanyu.com/',
      packages=['ybc_food'],
      package_data={'ybc_food': ['test.jpg', '*.py']},
      license='MIT',
      install_requires=['requests', 'ybc_config', 'ybc_exception']
      )