# FsForge - file system tests helper

`fsforge` - is a toolset defining fake or real filesystem layout.

Gives among others a functionality:
 - for creating artificial `fs` using `pyfakefs`.
 - for taking a snapshot of either real of faked file system.

In short it is some kind of syntax' extension to `pyfakefs` and
is intended to use with `pytest` framework. Allows for absolute
transparency in `fs` operations, so that any kind of tests: untit,
functional or end-to-end can be performed in memory - instead of
real hard disc operations (`SSD`s can breathe and relax), without any headache nor
enormous setup nor teardown.

The main difference against bare `pyfakefs` is that `fsforge` uses nice
and clean `dict` literals instead of lists of paths. It also allows for reverse
operation - to create the same kind of nested dictionary structure defining
given `fs` with just single function call.

Such a result is immediately ready to make assertions on it.

Works with python `2.7`, `3.4`, `3.5`, `3.6`, `3.7`, `pypy` and `pypy3`.
Created with `pyfakefs==3.4.3`.

# Usage
## Capture real or faked `fs` snapshot.

Let's use following structure originated in `/tmp/ex` for all further examples:

```
 bash>$ tree /tmp/ex
 /tmp/ex
 ├── dir_a
 │   ├── sub_empty_dir
 │   ├── sub_dir_with_a_file
 │   │   ├── app_dump.json
 │   │   └── file_1.txt
 │   └── file_2.txt
 ├── dir_b
 │   ├── special_file.txt
 │   └── file_4.bin
 ├── empty_dir
 └── special_file_2.txt
```
We can collect a snapshot of this layout with:

```python
import pprint
from fsforge import take_fs_snapshot

tree = take_fs_snapshot('/tmp/ex')
pprint.pprint(tree)
```

will output such a `tree`:
```python
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
```
### Meaning

The resulting `tree` is a pure `dict`.  `fsforge` uses magic
relation and similarity of directory to a python's dictionary.

Directories are recognized by being `dict` instances.
Any other value type in the `tree` is treat as a file.
`fsforge` distinguishes only `dict` (as directories)
and `non dict` (files) while traversing the tree.


## Create forged file system

Now `fsforge` can use such kind of `tree` to perform needed `pyfakefs`'
calls to recreate the structure in memory for some `pytest` tests:

```python
import os

from fsforge import create_fs

def test_that(fs):

    create_fs(fs, tree, "/tmp/ex"):

    # everything is now set up:
    assert os.path.isdir("/tmp/ex/dir_a/sub_dir_with_a_file")
    assert os.path.isfile("/tmp/ex/dir_a/file_2.txt")

```

In the code above:
 -  `fs` is a fixture automatically accessible in tests as soon as
    you have `pyfakefs` package installed. It can also be a
    `FakeFilesystem` object instance imported from `pyfakefs`.
 - `fs` could also be a `fsforge.RealFS` object. Real writes will be performed.
 -  `tree` is reused dictionary from previous code snippets
 -  `"/tmp/ex"` is a origin of "mount point" of given structure,
    `pyfakefs` will anchor items specified in `tree` to this path.


## Basic Workflow

The application you test may make some changes to given file system.
After some time you can collect a snapshot of the `fs` structure and
make needed assertions on the changes made to its state.

E.g.  probably some files were removed or created, some content appended. Whatever..
Of course you may not be interested with all of that, that's why there is:

## File Processors and Path Masking

The `take_fs_snapshot` function takes a file system  mask definition as an argument.
File processor is just a function provided by you taking given file path and returning
anything you need from that file, e.g. it's contents (or any processing result or `None`).

```python
def reader(file_path):
    with open(file_path, 'r') as file_:
        return file_.read()

def json_reader(file_path):
    content = json.loads(reader(file_path))
    return json.dumps(content["some section only"])
```

Assume we have a file system from `/tmp/ex` from beginning of this readme.
And we want to read:
-   whole contents of any file in `dir_b` whose name contains `file` substring
-   `app_dump.json` - in whatever directory but "some section only" is
    interesting
-   note existence of any files in the top dir
-   ignore existence of any other file

So let's create a mask and call it:

```python
from fsforge import iddle_file_processor

# iddle_file_processor returns None regardless of call argument, is used to note
# files existence (without that file is ignored and does not appear in the result tree)

mask = {
    'dir_b': {
        # any file containing 'file' substring
        '*file*': reader,
    },
    '**': {
        # any file named app_dump.json in whatever path
        'app_dump.json': json_reader,
    },
    # Note any file in top level directory (but don't read it)
    '*': iddle_file_processor,
}

result = take_fs_snapshot("/tmp/ex", mask)

from pprint import pprint
pprint(result)

{
    'dir_a': {
        'sub_empty_dir': {},
        'sub_dir_with_a_file': {
            'app_dump.json': '{"some section only": "its contents"}',
        },
    },
    'dir_b': {
        'app_dump.json': '{"some section only": "its contents in dir_b"},
        'special_file.txt': "distinguished content",
        'file_4.bin': "contents of file_4"
    },
    'empty_dir': {},
    'special_file_2.txt': None,
}
```

Does that result look similar? Yes, it's the same kind of tree, but files have strings instead of nones.
It can be used to recreate the `fs` with these strings as contents of the new files.
