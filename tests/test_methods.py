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


def test_caplog(caplog):
    logger = logging.getLogger('foobar')
    logger.info('this is to info')
    logger.debug('this is to debug')

    assert 'foobar INFO: this is to info\n' == caplog == str(caplog)
    assert 'foobar INFO: that is to info\n' == caplog(('this', 'that'))
    assert 'to info' in caplog
    assert repr(caplog) == "< caplog: 'foobar INFO: this is to info\\n'>"


def test_caplog_debug(caplog):
    caplog.set_different_level(foobar=logging.DEBUG)
    logger = logging.getLogger('foobar')
    logger.info('this is to info')
    logger.debug('this is to debug')

    assert 'foobar INFO: this is to info\nfoobar DEBUG: this is to debug\n' == caplog


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

def test_debug(debug):
    logger = logging.getLogger('foobar')
    logger.info('this is to info')
    logger.debug('this is to debug')
""")
    result = testdir.runpytest('-p', 'no:sugar', '-s')
    result.assert_outcomes(passed=1)
    _, stderr = capsys.readouterr()
    assert 'this is to debug' in stderr
