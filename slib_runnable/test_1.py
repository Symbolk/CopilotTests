import argparse
import datetime
import json
import logging
import os
import pathlib


DEFAULT_CHECKS = (
    {'name': 'repository', 'frequency': '2 weeks'},
    {'name': 'archives', 'frequency': '2 weeks'},
)
DEFAULT_PREFIX = '{hostname}-'


def parse_frequency(frequency):
    '''
    Given a frequency string with a number and a unit of time, return a corresponding
    datetime.timedelta instance or None if the frequency is None or "always".

    For instance, given "3 weeks", return datetime.timedelta(weeks=3)

    Raise ValueError if the given frequency cannot be parsed.
    '''
    if not frequency:
        return None

    frequency = frequency.strip().lower()

    if frequency == 'always':
        return None

    try:
        number, time_unit = frequency.split(' ')
        number = int(number)
    except ValueError:
        raise ValueError(f"Could not parse consistency check frequency '{frequency}'")

    if not time_unit.endswith('s'):
        time_unit += 's'

    if time_unit == 'months':
        number *= 4
        time_unit = 'weeks'
    elif time_unit == 'years':
        number *= 365
        time_unit = 'days'

    try:
        return datetime.timedelta(**{time_unit: number})
    except TypeError:
        raise ValueError(f"Could not parse consistency check frequency '{frequency}'")




def test_parse_frequency():
    """Check the correctness of parse_frequency
    """
    assert parse_frequency('1 day') == datetime.timedelta(days=1)
    assert parse_frequency('1 week') == datetime.timedelta(weeks=1)
    assert parse_frequency('1 month') == datetime.timedelta(weeks=4)
    assert parse_frequency('1 year') == datetime.timedelta(days=365)
    assert parse_frequency('1 day') == datetime.timedelta(days=1)
    assert parse_frequency('10 day') == datetime.timedelta(days=10)