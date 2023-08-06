#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.deco',
  description = 'Assorted decorator functions.',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20190526',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  include_package_data = True,
  install_requires = ['cs.pfx'],
  keywords = ['python2', 'python3'],
  license = 'GNU General Public License v3 (GPLv3)',
  long_description = 'Assorted decorator functions.\n\n## Function `decorator(deco)`\n\nWrapper for decorator functions to support optional arguments.\nThe actual decorator function ends up being called as:\n\n    deco(func, *da, **dkw)\n\nallowing `da` and `dkw` to affect the bahviour of the decorator `deco`.\n\nExamples:\n\n    @decorator\n    def deco(func, *da, kw=None):\n      ... decorate func subject to the values of da and kw\n    @deco\n    def func1(...):\n      ...\n    @deco(\'foo\', arg2=\'bah\')\n    def func2(...):\n      ...\n\n## Function `fmtdoc(func)`\n\nDecorator to replace a function\'s docstring with that string\nformatted against the function\'s module\'s __dict__.\n\nThis supports simple formatted docstrings:\n\n    ENVVAR_NAME = \'FUNC_DEFAULT\'\n\n    @fmtdoc\n    def func():\n        """Do something with os.environ[{ENVVAR_NAME}]."""\n        print(os.environ[ENVVAR_NAME])\n\nThis gives `func` this docstring:\n\n    Do something with os.environ[FUNC_DEFAULT].\n\n*Warning*: this decorator is intended for wiring "constants"\ninto docstrings, not for dynamic values. Use for other types\nof values should be considered with trepidation.\n\n## Function `observable_class(property_names, only_unequal=False)`\n\nClass decorator to make various instance attributes observable.\n\nParameters:\n* `property_names`:\n  an interable of instance property names to set up as\n  observable properties. As a special case a single `str` can\n  be supplied of only one attribute is to be observed.\n* `only_unequal`:\n  only call the observers if the new property value is not\n  equal to the previous proerty value. This requires property\n  values to be comparable for inequality.\n  Default: `False`, meaning that all updates will be reported.',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.deco'],
)
