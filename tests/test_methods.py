import logging
import os

from pytest_toolbox import gettree, mktree

pytest_plugins = 'pytester'


def test_mktree(tmpdir):
    mktree(tmpdir, {
        'foo': 'bar',
        'a_dir': {
            'f': 'X'
        }
    })
    assert tmpdir.join('foo').exists()
    assert tmpdir.join('foo').read_text('utf') == 'bar'
    assert tmpdir.join('a_dir').isdir()
    assert tmpdir.join('a_dir/f').read_text('utf') == 'X'


def test_deep(tmpdir):
    mktree(tmpdir, {
        'foo/bar': {
            'f': 'X'
        }
    })
    assert tmpdir.join('foo').isdir()
    assert tmpdir.join('foo/bar').isdir()
    assert tmpdir.join('foo/bar/f').read_text('utf') == 'X'


def test_gettree(tmpdir):
    tmpdir.join('foo').write_text('bar', 'utf8')
    assert {
        'foo': 'bar'
    } == gettree(tmpdir)


def test_gettree_truncate(tmpdir):
    tmpdir.join('foo').write_text('123456789', 'utf8')
    assert {
        'foo': '12...'
    } == gettree(tmpdir, max_len=5)


def test_smart_caplog(smart_caplog):
    logger = logging.getLogger('foobar')
    logger.info('this is to info')
    logger.debug('this is to debug')

    assert 'foobar INFO: this is to info\n' == smart_caplog == str(smart_caplog)
    assert 'foobar INFO: that is to info\n' == smart_caplog(('this', 'that'))
    assert 'to info' in smart_caplog
    assert repr(smart_caplog) == "< caplog: 'foobar INFO: this is to info\\n'>"


def test_caplog_change(smart_caplog):
    smart_caplog.set_loggers(log_names=('foo',), level=logging.WARNING, fmt='%(message)s')
    logger_foo = logging.getLogger('foo')
    logger_foo.info('this is to foo info')
    logger_foo.warning('this is to foo warning')
    logger_bar = logging.getLogger('bar')
    logger_bar.info('this is to bar info')
    logger_bar.warning('this is to bar warning')

    assert 'this is to foo warning\n' == smart_caplog


def test_caplog_debug(smart_caplog):
    smart_caplog.set_different_level(foobar=logging.DEBUG)
    logger = logging.getLogger('foobar')
    logger.info('this is to info')
    logger.debug('this is to debug')

    assert 'foobar INFO: this is to info\nfoobar DEBUG: this is to debug\n' == smart_caplog


def test_tmpworkdir(tmpworkdir):
    assert os.getcwd() == str(tmpworkdir)


def test_async_tests(testdir):
    testdir.makepyfile("""\
import asyncio

async def get_4():
    return 4

async def test_async(loop):
    assert isinstance(loop, asyncio.AbstractEventLoop)
    v = await get_4()
    assert v == 4
""")
    result = testdir.runpytest('-p', 'no:sugar')
    result.assert_outcomes(passed=1)


def test_debug(testdir, capsys):
    testdir.makepyfile("""\
import logging

def test_print_logs(print_logs):
    logger = logging.getLogger('foobar')
    logger.info('this is to info')
    logger.debug('this is to debug')
""")
    result = testdir.runpytest('-p', 'no:sugar', '-s')
    result.assert_outcomes(passed=1)
    _, stderr = capsys.readouterr()
    assert 'this is to debug' in stderr
