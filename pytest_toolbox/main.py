import asyncio
import contextlib
import io
import logging
import os
import re
from copy import copy

import pytest
from py._path.local import LocalPath


@contextlib.contextmanager
def loop_context(existing_loop=None):
    """
    context manager which creates an asyncio loop.

    :param existing_loop: if supplied this loop is passed straight through and no new loop is created.
    """
    if existing_loop:
        # loop already exists, pass it straight through
        yield existing_loop
    else:
        _loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

        yield _loop

        if not _loop.is_closed():  # pragma: no branch
            _loop.call_soon(_loop.stop)
            _loop.run_forever()
            _loop.close()
        asyncio.set_event_loop(None)


def pytest_pycollect_makeitem(collector, name, obj):
    """
    Fix pytest collecting for coroutines.
    """
    if collector.funcnamefilter(name) and asyncio.iscoroutinefunction(obj):
        return list(collector._genfunctions(name, obj))


def pytest_pyfunc_call(pyfuncitem):
    """
    Run coroutines in an event loop instead of a normal function call.
    """
    if asyncio.iscoroutinefunction(pyfuncitem.function):
        existing_loop = pyfuncitem.funcargs.get('loop', None)
        with loop_context(existing_loop) as _loop:
            testargs = {arg: pyfuncitem.funcargs[arg] for arg in pyfuncitem._fixtureinfo.argnames}

            task = _loop.create_task(pyfuncitem.obj(**testargs))
            _loop.run_until_complete(task)

        return True


@pytest.yield_fixture
def loop():
    """
    Yield fixture using loop_context()
    """
    with loop_context() as _loop:
        yield _loop


@pytest.yield_fixture
def tmpworkdir(tmpdir):
    """
    Create a temporary working working directory.
    """
    cwd = os.getcwd()
    os.chdir(tmpdir.strpath)

    yield tmpdir

    os.chdir(cwd)


def mktree(lp: LocalPath, d):
    """
    Create a tree of files from a dictionary of name > content lookups.
    """
    for name, content in d.items():
        _lp = copy(lp)

        parts = list(filter(bool, name.split('/')))
        for part in parts[:-1]:
            _lp = _lp.mkdir(part)
        _lp = _lp.join(parts[-1])

        if isinstance(content, dict):
            _lp.mkdir()
            mktree(_lp, content)
        else:
            _lp.write(content)


def gettree(lp: LocalPath, max_len=120):
    """
    Get a dict representing the file tree for a directory
    """
    assert lp.check()
    if lp.isdir():
        return {df.basename: gettree(df, max_len=max_len) for df in lp.listdir()}
    else:
        assert lp.isfile()
        content = lp.read_text('utf8')
        if max_len and len(content) > max_len:
            content = content[:max_len - 3] + '...'
        return content


class StreamLog:
    """
    Log stream object which allows one or more logs to be captured and tested.
    """
    def __init__(self, *log_names, level=logging.INFO, fmt='%(name)s %(levelname)s: %(message)s'):
        self.handler = None
        self.stream = io.StringIO()
        self.handler = logging.StreamHandler(stream=self.stream)
        self.loggers = []
        self._log_names = log_names or ('',)
        self._level = level
        self._fmt = fmt
        self.set_loggers()

    def set_loggers(self, *, log_names=None, level=None, fmt=None):
        if self.loggers:
            self.finish()
        if log_names is not None:
            self._log_names = log_names or ('',)
        if level is not None:
            self._level = level
        if fmt is not None:
            self._fmt = fmt
        self.loggers = [logging.getLogger(log_name) for log_name in self._log_names]
        self.handler.setFormatter(logging.Formatter(self._fmt))
        for logger in self.loggers:
            logger.disabled = False
            logger.addHandler(self.handler)
        self.set_level(self._level)

    def set_level(self, level):
        for logger in self.loggers:
            logger.setLevel(level)

    @classmethod
    def set_different_level(cls, **levels):
        for log_name, level in levels.items():
            logger = logging.getLogger(log_name)
            logger.setLevel(level)

    @property
    def log(self):
        self.stream.seek(0)
        return self.stream.read()

    def finish(self):
        for logger in self.loggers:
            logger.removeHandler(self.handler)

    def __call__(self, *normalisers):
        log = str(self)
        for pattern, repl in normalisers:
            log = re.sub(pattern, repl, log)
        return log

    def __eq__(self, other):
        return self.log == other

    def __contains__(self, item):
        return item in self.log

    def __str__(self):
        return self.log

    def __repr__(self):
        return '< caplog: {!r}>'.format(self.log)


@pytest.yield_fixture
def caplog():
    """
    Similar to pytest's "capsys" except logs are captured not stdout and stderr

    See StreamLog for details on configuration and tests for examples of usage.
    """
    stream_log = StreamLog()

    yield stream_log

    stream_log.finish()


@pytest.yield_fixture
def debug():
    """
    fixture which causes all arq logs to display. For debugging purposes only, should alwasy
    be removed before committing.
    """
    # TODO: could be extended to also work as a context manager and allow more control.
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('%(asctime)s %(name)14s %(levelname)7s: %(message)s', datefmt='%H:%M:%S'))
    logger = logging.getLogger('')
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    yield

    logger.removeHandler(handler)
    logger.setLevel(logging.NOTSET)
