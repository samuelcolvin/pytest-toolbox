pytest-toolbox
==============

|Build Status| |codecov.io| |PyPI Status| |license|

Copyright (C) 2016 Samuel Colvin

Numerous useful plugins for pytest.

Fixtures
--------

tmpworkdir
    Run the test with the working directory set to a temporary directory. Similar to the pytest plugin ``tmpdir``
    except working directory is changed.

caplog
    capture logs.

debug
    print all logs.

loop
    asyncio loop.

Methods
-------

(See below for usage examples).

mktree
    Create a tree of files from a dictionary.

gettree
    Return a dictionary depicting a directory tree.

Usage
-----

.. code:: python

    from pytest_toolbox import gettree, mktree

    def test_whatever(tmpworkdir):
        mktree(tmpworkdir, {
            'foobar.txt': 'has this content'
        })
        assert gettree(tmpworkdir) = {'foobar.txt': 'has this content'}

**TODO**


.. |Build Status| image:: https://travis-ci.org/samuelcolvin/pytest-toolbox.svg?branch=master
   :target: https://travis-ci.org/samuelcolvin/pytest-toolbox
.. |codecov.io| image:: http://codecov.io/github/samuelcolvin/pytest-toolbox/coverage.svg?branch=master
   :target: http://codecov.io/github/samuelcolvin/pytest-toolbox?branch=master
.. |PyPI Status| image:: https://img.shields.io/pypi/v/pytest-toolbox.svg?style=flat
   :target: https://pypi.python.org/pypi/pytest-toolbox
.. |license| image:: https://img.shields.io/pypi/l/pytest-toolbox.svg
   :target: https://github.com/samuelcolvin/pytest-toolbox
