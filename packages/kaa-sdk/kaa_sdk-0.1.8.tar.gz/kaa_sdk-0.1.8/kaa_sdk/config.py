import os
import json

from .file_utils import (is_kaa_dir_permissions_valid, KAA_CREDENTIALS_FILE, KAA_DIR, KAA_DEFAULT_CREDENTIALS,
                         KAA_CONFIG_FILE, KAA_DEFAULT_CONFIG)
from .exceptions import UnauthorizedFileAccessException
from .common import with_types


@with_types(str, str, str, str)
def set_credentials_file(uname=None, password=None, client_id=None, client_secret=None):
    r"""
    Creates or updates ~/.kaa/.credentials file on your local machine with given info.

    :param uname: kaa platform username
    :param password: kaa platform password
    :param client_id: your clientId
    :param client_secret: your client secret
    """
    if not is_kaa_dir_permissions_valid():
        raise UnauthorizedFileAccessException(KAA_DIR)

    creds = get_credentials()
    creds['username'] = uname
    creds['password'] = password
    creds['client_id'] = client_id
    creds['client_secret'] = client_secret

    with open(KAA_CREDENTIALS_FILE, 'w') as f:
        json.dump(creds, f, indent=4)


def get_credentials():
    if os.path.isfile(KAA_CREDENTIALS_FILE):
        with open(KAA_CREDENTIALS_FILE) as f:
            return json.load(f)
    else:
        return KAA_DEFAULT_CREDENTIALS


@with_types(str, str, str)
def set_config_file(host=None, auth_host=None, realm=None):
    r"""
    Creates or updates ~/.kaa/.config file on your local machine with given info.

    :param host: host of kaa-cluster
    :param auth_host: keycloak host
    :param realm: realm
    """
    if not is_kaa_dir_permissions_valid():
        raise UnauthorizedFileAccessException(KAA_DIR)

    configs = get_config()
    configs['host'] = host
    configs['realm'] = realm
    configs['auth_host'] = auth_host

    with open(KAA_CONFIG_FILE, 'w') as f:
        json.dump(configs, f, indent=4)


def get_config():
    if os.path.isfile(KAA_CONFIG_FILE):
        with open(KAA_CONFIG_FILE) as f:
            return json.load(f)
    else:
        return KAA_DEFAULT_CONFIG
