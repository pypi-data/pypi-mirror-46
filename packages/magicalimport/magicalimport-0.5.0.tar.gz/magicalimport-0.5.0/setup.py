# -*- coding:utf-8 -*-

import os
import sys


from setuptools import setup, find_packages
here = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(here, 'README.rst')) as f:
        README = f.read()
    with open(os.path.join(here, 'CHANGES.txt')) as f:
        CHANGES = f.read()
except IOError:
    README = CHANGES = ''


install_requires = [
]
if sys.version_info[0] == 2:
    install_requires.append("importlib2")

docs_extras = [
]

tests_require = [
]

testing_extras = tests_require + [
]

setup(name='magicalimport',
      version='0.5.0',
      description='importing a module by physical file path',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: Implementation :: CPython",
      ],
      keywords='import, physical address, file path',
      author="podhmo",
      author_email="ababjam61+github@gmail.com",
      url="https://github.com/podhmo/magicalimport",
      packages=find_packages(exclude=["magicalimport.tests"]),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      extras_require={
          'testing': testing_extras,
          'docs': docs_extras,
      },
      tests_require=tests_require,
      test_suite="magicalimport.tests",
      entry_points="""
""")

