#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.sqlalchemy_utils',
  description = 'Assorted utility functions to support working with SQLAlchemy.',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20190517',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Topic :: Database', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  include_package_data = True,
  install_requires = ['icontract', 'sqlalchemy', 'cs.py.func'],
  keywords = ['python2', 'python3'],
  license = 'GNU General Public License v3 (GPLv3)',
  long_description = 'Assorted utility functions to support working with SQLAlchemy.\n\n## Function `auto_session(func)`\n\nDecorator to run a function in a session is not presupplied.\n\n## Class `ORM`\n\nA convenience base class for an ORM class.\n\nThis defines a `.Base` attribute which is a new `DeclarativeBase`\nand provides various Session related convenience methods.\n\nSubclasses must define their own `.Session` factory in\ntheir own `__init__`, for example:\n\n    self.Session = sessionmaker(bind=engine)\n\n## Function `orm_auto_session(method)`\n\nDecorator to run a method in a session derived from `self.orm`\nif a session is not presupplied.\nIntended to assist classes with a `.orm` attribute.\n\n## Function `with_session(func, *a, orm=None, session=None, **kw)`\n\nCall `func(*a,session=session,**kw)`, creating a session if required.\n\nThis is the inner mechanism of `@auto_session` and\n`ORM.auto_session_method`.\n\nParameters:\n* `func`: the function to call\n* `a`: the positional parameters\n* `orm`: optional ORM class with a `.session()` context manager method\n* `session`: optional existing ORM session\n\nOne of `orm` or `session` must be not `None`; if `session`\nis `None` then one is made from `orm.session()` and used as\na context manager. The `session` is also passed to `func` as\nthe keyword parameter `session` to support nested calls.',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.sqlalchemy_utils'],
)
