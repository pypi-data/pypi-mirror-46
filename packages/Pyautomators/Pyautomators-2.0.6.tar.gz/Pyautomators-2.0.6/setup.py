# -*- coding: utf-8 -*-
from setuptools import setup,find_packages

setup(name='Pyautomators',
      version='2.0.6',
      url='',
      license='MIT',
      author='Kaue Bonfim',
      author_email='koliveirab@indracompany.com',
      description='Automation library for complete generation of testicle environment',
      packages=['Pyautomators',
                  'Pyautomators.compat',
                  'Pyautomators.contrib',
                  'Pyautomators.formatter',
      		'Pyautomators.reporter',
      		],
	install_requires=['parse-type', 'six', 'parse'],
      zip_safe=True,
      test_suite='test',
      long_description=open('README.md').read()
      )
      