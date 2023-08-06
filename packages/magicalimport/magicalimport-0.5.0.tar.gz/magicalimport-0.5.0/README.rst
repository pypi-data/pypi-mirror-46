magicalimport
========================================

.. image:: https://travis-ci.org/podhmo/magicalimport.svg?branch=master
  :target: https://travis-ci.org/podhmo/magicalimport

Importing a module from physical file path.

examples
----------------------------------------

these files are existed, then..

.. code-block:: bash

  $ tree
  .
  ├── a
  │   └── b
  │       └── c
  │           └── foo.py
  └── main.py

  4 directories, 3 files


a/b/c/foo.py

.. code-block:: python

  name = "foo"
  _age = "*secret*"

.. code-block:: python

  from magicalimport import import_from_physical_path

  # importing foo.py as the module named foo2
  foo = import_from_physical_path("./a/b/c/foo.py", as_="foo2")
  print(foo.name)

  # cached in sys.modules, so it is ok.
  import foo2
  print(foo2.name)


here option
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

  from magicalimport import import_from_physical_path

  import_from_physical_path("bar.py", here="/tmp/foo", as_="bar")

star import
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from magicalimport import import_from_physical_path
   from magicalimport import expose_all_members

   # something of like a `from foo import *`
   expose_all_members(import_from_physical_path("./a/b/c/foo.py"))
   print(name)  # "foo"
   # print(_age)  # NameError.. because expose_all_members() doesn't expose the symbols started by "_"

   # or
   from magicalimport import expose_members
   expose_members(import_from_physical_path("./a/b/c/foo.py"), members=["_age"])
   print(_age)  # "*secret*"
