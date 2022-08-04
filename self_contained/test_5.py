def is_none_string(val: any) -> bool:
    """Check if a string represents a None value."""
    if not isinstance(val, str):
        return False

    return val.lower() == 'none'

def test_is_none_string():
    """
    Check the corretness of is_none_string
    """
    assert is_none_string('None')==True
    assert is_none_string('none')==True
    assert is_none_string('not none')==False
    assert is_none_string(None)==False
    assert is_none_string('')==False
    assert is_none_string(' ')==False

