# -*- coding: utf-8 -*-

"""
Licensed under GPLv3, see LICENSE.txt for terms and conditions.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import os, sys
from setuptools import setup, find_packages

version = '0.0.1'

LONG_DESCRIPTION = 'This is a temporary placeholder'
app_name = 'rorolang'

setup(
      name = app_name,
      version = version,

      author = '',
      description = LONG_DESCRIPTION,
      long_description = LONG_DESCRIPTION,
      platforms = ['OS Independent'],
      license = 'GPLv3',
      zip_safe = False,

      classifiers = [
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Environment :: X11 Applications',
        'Environment :: MacOS X',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Other Audience',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        ],
)
