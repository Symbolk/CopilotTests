import pkg_resources
import argparse
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
    assert parser_flags(argparse.ArgumentParser()) == '-h --help'
    assert parser_flags(argparse.ArgumentParser(add_help=False)) == ''
    assert parser_flags(argparse.ArgumentParser(prog='test')) == '-h --help'
    assert parser_flags(argparse.ArgumentParser(prog='test', add_help=False)) == ''
    assert parser_flags(argparse.ArgumentParser(prog='test', description='test')) == '-h --help'
    assert parser_flags(argparse.ArgumentParser(prog='test', description='test', add_help=False)) == ''
    assert parser_flags(argparse.ArgumentParser(prog='test', description='test', epilog='test')) == '-h --help'