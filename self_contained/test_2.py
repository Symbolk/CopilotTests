
def replace_dots(value, arg):
    """Replaces all values of '.' to arg from the given string"""
    return value.replace(".", arg)

def test_replace_dots():
    """
    Check the corretness of replace_dots
    """
    assert  replace_dots("test.txt", ".") == "test.txt"