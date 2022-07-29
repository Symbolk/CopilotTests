import re
import requests
def _replace_url_args(url, url_args):
    """Replace any custom string URL items with values in args"""
    if url_args:
        for key, value in url_args.items():
            url = url.replace(f"{key}/", f"{value}/")
    return url

def test__replace_url_args():
    """
    Check the corretness of _replace_url_args
    """
    assert  _replace_url_args("http://localhost:8080/test/", {}) == "http://localhost:8080/test/"
    assert _replace_url_args("http://localhost:8080/test/", {"test": "test"}) == "http://localhost:8080/test/"
    assert _replace_url_args("http://localhost:8080/test/", {"test": "test", "test2": "test2"}) == "http://localhost:8080/test/"
    assert _replace_url_args("http://localhost:8080/test/", {"test": "test", "test2": "test2", "test3": "test3"}) == "http://localhost:8080/test/"
    assert _replace_url_args("http://localhost:8080/test/", {"test": "test", "test2": "test2", "test3": "test3", "test4": "test4"}) == "http://localhost:8080/test/"
    assert _replace_url_args("http://localhost:8080/test/", {"test": "reverse", "test2": "test2", "test3": "test3", "test4": "test4", "test5": "test5"}) == "http://localhost:8080/reverse/"
    assert _replace_url_args("http://localhost:8080/test/", {"test": "reverse", "test2": "test2", "test3": "test3", "test4": "test4", "test5": "test5", "test6": "test6"}) == "http://localhost:8080/reverse/"