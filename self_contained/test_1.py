import os
import os.path
from urllib.parse import quote_plus, unquote_plus

def strip_root(path, root):
    """Remove root from path, throw exception on failure."""
    root = root.rstrip(os.sep)  # ditch any trailing path separator
    if os.path.commonprefix((path, root)) == root:
        return os.path.relpath(path, start=root)
    raise Exception("Path %s is not in root %s" % (path, root))

def test_strip_root():
    """
    Check the corretness of strip_root
    """
    assert strip_root("/home/user/file.txt", "/home/user") == "file.txt"
    assert strip_root("/home/user/file.txt", "/home/user/") == "file.txt"
    
    