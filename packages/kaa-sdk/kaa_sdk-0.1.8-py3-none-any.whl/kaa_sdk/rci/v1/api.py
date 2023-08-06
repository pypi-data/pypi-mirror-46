from ...config import get_config
from ...token import get_access_token
from ...common import with_types

import requests

API_VERSION = "v1"
SERVICE_NAME = "rci"


@with_types(str, str, dict)
def execute(endpoint_id, command_type, command):
    r"""
    Invokes command on the endpoint and returns its result in a response. Body can be any valid json that is meaningful
     for the target endpoint.

    :param endpoint_id: Unique endpoint identifier.
    :param command_type: Represents the type of the command client wants to invoke on the endpoint.
     Command type MUST be a non-empty alpha-numeric string identifying the command type to the endpoint.
    :param command: json-formatted command
    :return: command invocation result
    """
    host = get_config()['host']
    token = get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    resp = requests.post(
        f'https://{host}/{SERVICE_NAME}/api/{API_VERSION}/endpoints/{endpoint_id}/commands/{command_type}',
        headers=headers,
        json=command)
    resp.raise_for_status()

    return resp.json()
