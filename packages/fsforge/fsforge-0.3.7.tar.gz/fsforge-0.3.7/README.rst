FsForge - file system tests helper
==================================

``fsforge`` - is a toolset defining fake or real filesystem layout.

Gives among others a functionality:

-  for creating artificial ``fs`` using ``pyfakefs``.
-  for taking a snapshot of either real of faked file system.

In short it is some kind of syntax' extension to ``pyfakefs`` and is
intended to use with ``pytest`` framework. Allows for absolute
transparency in ``fs`` operations, so that any kind of tests: untit,
functional or end-to-end can be performed in memory - instead of real
hard disc operations (``SSD``\ s can breathe and relax), without any
headache nor enormous setup nor teardown.

The main difference against bare ``pyfakefs`` is that ``fsforge`` uses
nice and clean ``dict`` literals instead of lists of paths. It also
allows for reverse operation - to create the same kind of nested
dictionary structure defining given ``fs`` with just single function
call.

Such a result is immediately ready to make assertions on it.

Works with python ``2.7``, ``3.4``, ``3.5``, ``3.6``, ``3.7``, ``pypy``
and ``pypy3``. Created with ``pyfakefs==3.4.3``.

Usage
=====

.. _capture-real-or-faked-fs-snapshot:

Capture real or faked ``fs`` snapshot.
--------------------------------------

Let's use following structure originated in ``/tmp/ex`` for all further
examples:

::

    bash>$ tree /tmp/ex
    /tmp/ex
    ├── dir_a
    │   ├── sub_empty_dir
    │   ├── sub_dir_with_a_file
    │   │   ├── app_dump.json
    │   │   └── file_1.txt
    │   └── file_2.txt
    ├── dir_b
    │   ├── special_file.txt
    │   └── file_4.bin
    ├── empty_dir
    └── special_file_2.txt

We can collect a snapshot of this layout with:

.. code:: python

   import pprint
   from fsforge import take_fs_snapshot

   tree = take_fs_snapshot('/tmp/ex')
   pprint.pprint(tree)

will output such a ``tree``:

.. code:: python

    {
        'dir_a': {
            'sub_empty_dir': {},
            'sub_dir_with_a_file': {
                'app_dump.json': None,
                'file_1.txt': None
            },
            'file_2.txt': None,
        },
        'dir_b': {
            'app_dump.json': None,
            'special_file.txt': None,
            'file_4.bin': None
        },
        'empty_dir': {},
        'special_file_2.txt`: None
    }

Meaning
~~~~~~~

The resulting ``tree`` is a pure ``dict``. ``fsforge`` uses magic
relation and similarity of directory to a python's dictionary.

Directories are recognized by being ``dict`` instances. Any other value
type in the ``tree`` is treat as a file. ``fsforge`` distinguishes only
``dict`` (as directories) and ``non dict`` (files) while traversing the
tree.

Create forged file system
-------------------------

Now ``fsforge`` can use such kind of ``tree`` to perform needed
``pyfakefs``' calls to recreate the structure in memory for some
``pytest`` tests:

.. code:: python

   import os

   from fsforge import create_fs

   def test_that(fs):

       create_fs(fs, tree, "/tmp/ex"):

       # everything is now set up:
       assert os.path.isdir("/tmp/ex/dir_a/sub_dir_with_a_file")
       assert os.path.isfile("/tmp/ex/dir_a/file_2.txt")

In the code above:

-  ``fs`` is a fixture automatically accessible in tests as soon as you
   have ``pyfakefs`` package installed. It can also be a \`FakeFilesyst
