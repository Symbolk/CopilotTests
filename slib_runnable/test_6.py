import io
import os
import re



def _resolve_string(matcher):
    '''
    Get the value from environment given a matcher containing a name and an optional default value.
    If the variable is not defined in environment and no default value is provided, an Error is raised.
    '''
    name, default = matcher.group("name"), matcher.group("default")
    out = os.getenv(name, default=default)
    if out is None:
        raise ValueError("Cannot find variable ${name} in envivonment".format(name=name))
    return out




def test__resolve_string():
    """Check the correctness of _resolve_string
    """
    assert _resolve_string(re.compile(r"\$\{(?P<name>[a-zA-Z0-9_]+)(?P<default>\:.+)?\}").match("${name}")) == "name"