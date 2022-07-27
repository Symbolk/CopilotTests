import pkg_resources
def parser_flags(parser):
    '''
    Given an argparse.ArgumentParser instance, return its argument flags in a space-separated
    string.
    '''
    return ' '.join(option for action in parser._actions for option in action.option_strings)

def test_parser_flags():
    """
    Check the corretness of parser_flags
    """