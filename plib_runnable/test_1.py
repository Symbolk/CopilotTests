from __future__ import absolute_import, division, print_function

__metaclass__ = type
import io
import yaml

from ansible.module_utils.six import PY3
# from ansible.parsing.yaml.loader import AnsibleLoader
from ansible.parsing.yaml.dumper import AnsibleDumper


def _dump_string(obj, dumper=None):
    """Dump to a py2-unicode or py3-string"""
    if PY3:
        return yaml.dump(obj, Dumper=dumper)
    else:
        return yaml.dump(obj, Dumper=dumper, encoding=None)



def test__dump_string():
    """Check the correctness of _dump_string
    """
    assert _dump_string({"a": 1, "b": 2},dumper=AnsibleDumper) == "a: 1\nb: 2\n"
    assert _dump_string({"a": 1, "b": 2,"c":3,},dumper=AnsibleDumper) == "a: 1\nb: 2\nc: 3\n"
    assert _dump_string({"a": 1, "b": 2,"d":3,},dumper=AnsibleDumper) == "a: 1\nb: 2\nd: 3\n"
    assert _dump_string({"f": 1, "b": 2,"d":3,},dumper=AnsibleDumper) == "b: 2\nd: 3\nf: 1\n"
    assert _dump_string({1,2,3},dumper=AnsibleDumper) == "!!set\n1: null\n2: null\n3: null\n"
    assert _dump_string([1,2,3],dumper=AnsibleDumper) == "- 1\n- 2\n- 3\n"