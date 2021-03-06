#!/usr/bin/env python
import os
from setuptools import setup

project_dir = os.path.abspath(os.path.dirname(__file__))

long_descriptions = []
for rst in ('README.rst', 'LICENSE.rst'):
    with open(os.path.join(project_dir, rst), 'r') as f:
        long_descriptions.append(f.read())

setup(name='iotrelay-influxdb',
      version='1.7.1',
      description='InfluxDB handler module for iotrelay',
      long_description='\n\n'.join(long_descriptions),
      author='Emmanuel Levijarvi',
      author_email='emansl@gmail.com',
      url='https://github.com/eman/iotrelay-influxdb',
      license='BSD',
      py_modules=['iotrelay_influxdb'],
      test_suite='tests',
      install_requires=['iotrelay>=1.2', 'influxdb>=3.0.0'],
      tests_require=['iotrelay>=1.2', 'influxdb>=3.0.0'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Topic :: Home Automation',
          'Topic :: Utilities',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.7',
      ],
      keywords='influxdb IoT',
      entry_points={
          'iotrelay': ['handler=iotrelay_influxdb:Handler']
      })
