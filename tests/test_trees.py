pytest_plugins = 'pytester'


def test_mktree(testdir):
    testdir.makepyfile("""\
import logging
from pytest_toolbox import gettree, mktree

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

def test_gettree(tmpdir):
    tmpdir.join('foo').write_text('bar', 'utf8')
    assert {
        'foo': 'bar'
    } == gettree(tmpdir)

def test(caplog):
    logger = logging.getLogger('foobar')
    logger.info('this is to info')
    logger.debug('this is to debug')

    assert 'foobar INFO: this is to info\\n' == caplog
""")
    result = testdir.runpytest('-p', 'no:sugar')
    result.assert_outcomes(passed=3, failed=0)
