#
# Copyright (C) 2015  FreeIPA Contributors see COPYING for license
#

"""
CA installer module
"""

from __future__ import print_function, absolute_import

import enum
import logging
import os.path

import six

from ipalib.constants import IPA_CA_CN
from ipalib import api, errors, x509
from ipapython.dn import DN
from ipalib import api, errors, x509


if six.PY3:
    unicode = str

VALID_SUBJECT_BASE_ATTRS = {
    'st', 'o', 'ou', 'dnqualifier', 'c', 'serialnumber', 'l', 'title', 'sn',
    'givenname', 'initials', 'generationqualifier', 'dc', 'mail', 'uid',
    'postaladdress', 'postalcode', 'postofficebox', 'houseidentifier', 'e',
    'street', 'pseudonym', 'incorporationlocality', 'incorporationstate',
    'incorporationcountry', 'businesscategory',
}
VALID_SUBJECT_ATTRS = {'cn'} | VALID_SUBJECT_BASE_ATTRS

logger = logging.getLogger(__name__)

external_cert_file = None
external_ca_file = None

def lookup_random_serial_number_version(api):
    """
    Retrieve the random serial number version number from the
    remote server.

    If the value is > 0 then RSN was enabled. Return the raw
    value for future-proofing in case version-specific decisions
    need to be made.

    Returns 0 if RSN is not enabled or otherwise not available.
    """
    dn = DN(('cn', IPA_CA_CN), api.env.container_ca, api.env.basedn)
    version = 0
    try:
        # we do not use api.Command.ca_show because it attempts to
        # talk to the CA (to read certificate / chain), but the RA
        # backend may be unavailable (ipa-replica-install) or unusable
        # due to RA Agent cert not yet created (ipa-ca-install).
        entry = api.Backend.ldap2.get_entry(dn)

        # If the attribute doesn't exist then the remote didn't
        # enable RSN.
        if 'ipacarandomserialnumberversion' in entry:
            version = int(entry['ipacarandomserialnumberversion'][0])
    except (errors.NotFound, KeyError):
        # if the entry doesn't exist then the remote doesn't support
        # RSN so there is nothing to do.
        pass

    return version



def test_lookup_random_serial_number_version():
    """Check the correctness of lookup_random_serial_number_version
    """
    assert lookup_random_serial_number_version(api=api) == 0