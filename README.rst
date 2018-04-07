pytest-toolbox
==============

|Build Status| |codecov.io| |PyPI Status| |license|

Copyright (C) 2016 Samuel Colvin

Numerous useful plugins for pytest.

Fixtures
--------

``tmpworkdir``
    Run the test with the working directory set to a temporary directory. Similar to the pytest plugin ``tmpdir``
    except working directory is changed.

``smart_caplog``
    capture logs with a smarter interface than pytest's native ``caplog``

``print_logs``
    print all logs.

``loop``
    asyncio loop.

Methods
-------

(See below for usage examples).

``mktree``
    Create a tree of files from a dictionary.

``gettree``
    Return a dictionary depicting a directory tree.


Comparison Objects
------------------

All can be imported from ``pytest_toolbox.comparison``.

``CloseToNow``
    check that a date (or date-like object) is close to now

``AnyInt``
    check tests that an object is an int

``RegexStr``
    check that a string matches the regex

``IsUUID``
    that that an object is an instance of ``UUID``.

Used with equals as in ``my_date == CloseToNow()``, these are useful when checking objects which contain
a few unknown values are as expected

Eg.

.. code-block:: python

   assert {
       'details': {
           'user': 'foobar@example.com',
           'id': AnyInt(),
           'published': False,
           'event': 'an example',
           'created_ts': CloseToNow(),
       },
       'other_thing': [
           ...
       ],
       ...
   } == obj

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
