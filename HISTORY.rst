.. :changelog:

History
-------

0.5.0 (2018-09-02)
------------------
* remove ``loop`` fixture and stop coroutine collection, you should use ``pytest-aiohttp`` instead

0.4.0 (2018-04-07)
------------------
* add comparison classes
* rename ``caplog`` > ``smart_caplog``
* rename ``debug`` > ``print_logs``
* updates
* remove python 3.5 support, now 3.6 only due to pydantic requirement

0.3.0 (2017-03-11)
------------------
* check for un-awaited coroutines


0.2.0 (2017-02-11)
------------------
* tweaks to logging
* cleaner loop teardown
* update dependencies
