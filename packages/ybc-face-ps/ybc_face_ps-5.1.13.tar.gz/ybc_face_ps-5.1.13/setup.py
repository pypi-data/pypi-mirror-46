#!/usr/bin/env python

from distutils.core import setup

setup(name='ybc_face_ps',
      version='5.1.13',
      description='Face Control.',
      long_description='Face Control.',
      author='hurs',
      author_email='hurs@fenbi.com',
      keywords=['python', 'face', 'ps'],
      url='http://pip.zhenguanyu.com/',
      packages=['ybc_face_ps'],
      package_data={'ybc_face_ps': ['test.jpg', '*.py']},
      license='MIT',
      install_requires=['requests', 'ybc_config', 'ybc_exception']
      )