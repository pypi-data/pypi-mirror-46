#!/usr/bin/env python

from distutils.core import setup

setup(name='elitecode',
		scripts=['bin/funniest-joke'],
      version='1.6',
      description='Strategically Shuffling Leetcode Questions to Optimize DS&A Study Time',
      author='Christopher Lambert',
      author_email='lambertcr@outlook.com',
      url='https://github.com/theriley106/EliteCode',
      license='MIT',
      packages=['elitecode'],
      install_requires=['requests']
     )