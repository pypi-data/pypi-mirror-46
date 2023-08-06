#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name='webscreenshot',
      version='2.3',
      description='A simple script to screenshot a list of websites',
      long_description_content_type='text/markdown; charset=UTF-8;',
      long_description=open('webscreenshot/README.md').read(),
      url='https://github.com/maaaaz/webscreenshot',
      author='Thomas D.',
      author_email='tdebize@mail.com',
      license='LGPL',
      classifiers=[
        'Topic :: Security',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7'
      ],
      keywords='webscreenshot web screenshot phantomjs chrome chromium firefox lazy rendering',
      packages=find_packages(),
      install_requires=['argparse', 'future'],
      python_requires='>=2.7',
      entry_points={
        'console_scripts': ['webscreenshot=webscreenshot.webscreenshot:main'],
      },
      include_package_data=True)