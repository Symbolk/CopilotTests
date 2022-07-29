import collections
import copy
import json
import logging
import os
import sys
import time
from queue import Queue
from subprocess import CalledProcessError

import colorama
from matplotlib.collections import Collection
import pkg_resources


from borgmatic.config import checks, collect, convert, validate

logger = logging.getLogger(__name__)

LEGACY_CONFIG_PATH = '/etc/borgmatic/config'


def load_configurations(config_filenames, overrides=None, resolve_env=True):
    '''
    Given a sequence of configuration filenames, load and validate each configuration file. Return
    the results as a tuple of: dict of configuration filename to corresponding parsed configuration,
    and sequence of logging.LogRecord instances containing any parse errors.
    '''
    # Dict mapping from config filename to corresponding parsed config dict.
    configs = collections.OrderedDict()
    logs = []

    # Parse and load each configuration file.
    for config_filename in config_filenames:
        try:
            configs[config_filename] = validate.parse_configuration(
                config_filename, validate.schema_filename(), overrides, resolve_env
            )
        except PermissionError:
            logs.extend(
                [
                    logging.makeLogRecord(
                        dict(
                            levelno=logging.WARNING,
                            levelname='WARNING',
                            msg='{}: Insufficient permissions to read configuration file'.format(
                                config_filename
                            ),
                        )
                    ),
                ]
            )
        except (ValueError, OSError, validate.Validation_error) as error:
            logs.extend(
                [
                    logging.makeLogRecord(
                        dict(
                            levelno=logging.CRITICAL,
                            levelname='CRITICAL',
                            msg='{}: Error parsing configuration file'.format(config_filename),
                        )
                    ),
                    logging.makeLogRecord(
                        dict(levelno=logging.CRITICAL, levelname='CRITICAL', msg=error)
                    ),
                ]
            )

    return (configs, logs)


def test_load_configurations():
    """Check the correctness of load_configurations
    """
    
    assert load_configurations(['/etc/borgmatic/config'])[0] == collections.OrderedDict()