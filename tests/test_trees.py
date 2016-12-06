import logging

from pytest_toolbox import gettree, mktree


def test_mktree(tmpdir):
    mktree(tmpdir, {
        'foo': 'bar'
    })
    assert tmpdir.join('foo').exists()
    assert tmpdir.join('foo').read_text('utf') == 'bar'


def test_gettree(tmpdir):
    tmpdir.join('foo').write_text('bar', 'utf8')
    assert {
        'foo': 'bar'
    } == gettree(tmpdir)


def test_caplog(caplog):
    logger = logging.getLogger('foobar')
    logger.info('this is to info')
    logger.debug('this is to debug')

    assert 'foobar INFO: this is to info\n' == caplog
