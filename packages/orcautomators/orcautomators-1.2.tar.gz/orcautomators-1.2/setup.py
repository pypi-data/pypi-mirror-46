# -*- coding: utf-8 -*-
from setuptools import setup,find_packages

setup(name='orcautomators',
      version='1.2',
      url='',
      license='Indra Company',
      author='Kaue Bonfim',
      author_email='koliveirab@indracompany.com',
      description='Orchestration Library for Tests',
      packages=['orcautomators',],
	install_requires=['pyyaml==3.12', 'Pyautomators', 'argparse'],
      zip_safe=True,
      test_suite='test',
      long_description=open('README.md').read())