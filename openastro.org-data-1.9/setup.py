#!/usr/bin/env python

from distutils.core import setup, Extension
import glob, os.path, sys

pre_data_files = [
	('share/openastro.org', ['geonames.sql','famous.sql']),
	('share/swisseph', glob.glob('swisseph/*.*') )
	]

setup(name='OpenAstro.org Data Files',
      version='1.9',
      description='Open Source Astrology',
      author='Pelle van der Scheer',
      author_email='pellesimon@gmail.com',
      url='http://www.openastro.org',
      license='GPL',
      data_files=pre_data_files
     )
