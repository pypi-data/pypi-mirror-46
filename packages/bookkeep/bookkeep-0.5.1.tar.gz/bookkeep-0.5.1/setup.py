# -*- coding: utf-8 -*-
"""
Created on Sun Dec 30 18:42:27 2018

@author: yoelr
"""

from setuptools import setup

setup(
      name = 'bookkeep',
      packages = ['bookkeep'],
      license='MIT',
      version = '0.5.1',
      description = 'keep track of units and measurement bounds.',
      long_description=open('README.rst').read(),
      author = 'Yoel Cortes-Pena',
      install_requires=['numpy', 'pandas', 'pint'],
      package_data = {'bookkeep': ['my_units_defs.txt']},
      platforms=["Windows"],
      author_email = 'yoelcortes@gmail.com',
      url = 'https://github.com/yoelcortes/bookkeep',
      download_url = 'https://github.com/yoelcortes/bookkeep.git'
      )
      