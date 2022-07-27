import collections
import io
import os
import re

INDENT = 4
SEQUENCE_INDENT = 2



def write_configuration(config_filename, rendered_config, mode=0o600, overwrite=False):
    '''
    Given a target config filename and rendered config YAML, write it out to file. Create any
    containing directories as needed. But if the file already exists and overwrite is False,
    abort before writing anything.
    '''
    if not overwrite and os.path.exists(config_filename):
        return FileExistsError
        # raise FileExistsError(
        #     '{} already exists. Aborting. Use --overwrite to replace the file.'.format(
        #         config_filename
        #     )
        # )

    try:
        os.makedirs(os.path.dirname(config_filename), mode=0o700)
    except (FileExistsError, FileNotFoundError):
        pass

    with open(config_filename, 'w') as config_file:
        config_file.write(rendered_config)

    os.chmod(config_filename, mode)
    return rendered_config


def test_write_configuration():
    """Check the correctness of write_configuration
    """
    assert write_configuration('test.yaml', 'test', overwrite=True) == 'test'
    assert write_configuration('test.yaml', 'test', overwrite=False) == FileExistsError
    assert write_configuration('test.yaml', 'hhhhh', overwrite=True) == 'hhhhh'
    assert write_configuration('test.yaml', 'hhhhh', overwrite=False) == FileExistsError