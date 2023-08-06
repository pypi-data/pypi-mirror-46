import os

KAA_DIR = os.getenv('KAA_DIR', os.path.join(os.path.expanduser('~'), '.kaa'))
KAA_CREDENTIALS_FILE = os.path.join(KAA_DIR, '.credentials')
KAA_CONFIG_FILE = os.path.join(KAA_DIR, '.config')
TEST_FILE = os.path.join(KAA_DIR, '.test_file')


KAA_DEFAULT_CREDENTIALS = {
    "username": ' ',
    "password": ' ',
    "client_id": ' ',
    "client_secret": ' ',
    "grant_type": "password"
}

KAA_DEFAULT_CONFIG = {
    "auth_host": ' ',
    "host": ' ',
    "realm": ' '
}

_dir_permissions = None


def is_kaa_dir_permissions_valid():
    global _dir_permissions

    if not _dir_permissions:
        _dir_permissions = _permissions()

    return _dir_permissions


def _permissions():
    try:
        if not os.path.exists(KAA_DIR):
            os.mkdir(KAA_DIR)
        with open(TEST_FILE, 'w') as f:
            f.write('Just some text')
        os.remove(TEST_FILE)
        return True
    except:
        return False

