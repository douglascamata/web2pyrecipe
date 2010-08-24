# -*- coding: utf-8 -*-
"""
This module contains the tool of web2pyrecipe
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '1.0'

long_description = (
    read('README.txt')
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' +
    read('web2pyrecipe', 'recipe', 'web2pyrecipe', 'README.txt')
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
   'Download\n'
    '********\n'
    )
entry_point = 'web2pyrecipe.recipe.web2pyrecipe:Recipe'
entry_points = {"zc.buildout": ["default = %s" % entry_point]}

tests_require=['zope.testing', 'zc.buildout']

setup(name='web2pyrecipe',
      version=version,
      description="A web2py recipe for buildout.",
      long_description=long_description,
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Zope Public License',
        ],
      keywords='',
      author='Douglas Camata',
      author_email='d.camata@gmail.com',
      url='http://http://github.com/douglascamata/web2pyrecipe',
      license='ZPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['web2pyrecipe', 'web2pyrecipe.recipe'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'zc.buildout'
                        # -*- Extra requirements: -*-
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite = 'web2pyrecipe.recipe.web2pyrecipe.tests.test_docs.test_suite',
      entry_points=entry_points,
      )

