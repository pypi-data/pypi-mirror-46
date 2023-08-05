#!/usr/bin/env python

from distutils.core import setup

setup(name='ybc_face',
      version='5.1.15',
      description='Face detection and analysis.',
      long_description='Face detection and analysis.',
      author='hurs',
      author_email='hurs@fenbi.com',
      keywords=['python', 'face', 'detection', 'recognition'],
      url='http://pip.zhenguanyu.com/',
      packages=['ybc_face'],
      package_data={'ybc_face': ['*.jpg', '*.py']},
      license='MIT',
      install_requires=['requests', 'ybc_config', 'ybc_exception']
      )
