import copy
import logging
import re



logger = logging.getLogger(__name__)


MAKE_FLAGS_EXCLUDES = ('repository', 'archive', 'successful', 'paths', 'find_paths')

def make_find_paths(find_paths):
    '''
    Given a sequence of path fragments or patterns as passed to `--find`, transform all path
    fragments into glob patterns. Pass through existing patterns untouched.

    For example, given find_paths of:

      ['foo.txt', 'pp:root/somedir']

    ... transform that into:

      ['sh:**/*foo.txt*/**', 'pp:root/somedir']
    '''

    return tuple(
        find_path
        if re.compile(r'([-!+RrPp] )|(\w\w:)').match(find_path)
        else f'sh:**/*{find_path}*/**'
        for find_path in find_paths
    )



def test_make_find_paths():
    """Check the correctness of make_find_paths
    """
    assert make_find_paths(('foo.txt', 'pp:root/somedir')) == ('sh:**/*foo.txt*/**', 'pp:root/somedir')
    assert make_find_paths(('foo.txt', 'pp:root/somedir', '-R')) == ('sh:**/*foo.txt*/**', 'pp:root/somedir', 'sh:**/*-R*/**')
    assert make_find_paths(('foo.txt', 'pp:root/somedir', '-R', '-r')) == ('sh:**/*foo.txt*/**', 'pp:root/somedir', 'sh:**/*-R*/**', 'sh:**/*-r*/**')
    assert make_find_paths(('foo.txt', 'pp:root/somedir', '-R', '-r', '-P')) == ('sh:**/*foo.txt*/**', 'pp:root/somedir', 'sh:**/*-R*/**', 'sh:**/*-r*/**', 'sh:**/*-P*/**')
    assert make_find_paths(('foo.txt', 'pp:root/somedir', '-R', '-r', '-P', '-p')) == ('sh:**/*foo.txt*/**', 'pp:root/somedir', 'sh:**/*-R*/**', 'sh:**/*-r*/**', 'sh:**/*-P*/**', 'sh:**/*-p*/**')