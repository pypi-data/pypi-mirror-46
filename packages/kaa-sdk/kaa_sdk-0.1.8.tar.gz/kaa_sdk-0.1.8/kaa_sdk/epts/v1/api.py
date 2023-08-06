from ...config import get_config
from ...token import get_access_token
from ...common import with_types
from datetime import datetime

import requests

API_VERSION = "v1"
SERVICE_NAME = "epts"


@with_types(list)
def get_time_series_config(application_names=None):
    r"""
    Returns configurations of all time series.

    :param application_names: Application name, one or multiple. If not specified,
     the data is returned for all available applications.
    :return: json with time series configuration
    """

    host = get_config()['host']
    token = get_access_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "applicationNames": application_names
    }
    resp = requests.get(f'https://{host}/{SERVICE_NAME}/api/{API_VERSION}/time-series/config',
                        params=params, headers=headers)
    resp.raise_for_status()

    return resp.json()


def get_time_series(app_name, time_series_names, from_date, to_date, endpoint_id=None, sort='ASC'):
    r"""
    Returns time series data points within the specified time range ordered by timestamp and grouped by endpoints.

    :param app_name: Application name
    :param time_series_names: One or more time series names.
    :param from_date: Start date to retrieve data points.
    :param to_date: End date to retrieve data points.
    :param endpoint_id: One or more endpoint IDs. If not specified, data is returned for all available endpoints.
    :param sort: Sorting order by timestamp. (one of 'ASC', 'DESC' - default: 'ASC')
    :return: json with time-series data
    """
    host = get_config()['host']
    token = get_access_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "timeSeriesName": time_series_names,
        "endpointId": endpoint_id,
        "fromDate": f"{from_date.isoformat()}Z",
        "toDate": f"{to_date.isoformat()}Z",
        "sort": sort
    }

    resp = requests.get(f'https://{host}/{SERVICE_NAME}/api/{API_VERSION}/applications/{app_name}/time-series/data',
                        params=params, headers=headers)
    resp.raise_for_status()

    return resp.json()


@with_types(str, list)
def get_last_time_series(app_name, time_series_names, endpoint_id=None):
    r"""
    Returns the most recent data points for time series for endpoint(s).

    :param app_name: Application name
    :param time_series_names: Time series names, one or multiple.
    :param endpoint_id: Endpoint ID, one or multiple. If not specified, the data is returned for all available endpoints.
    :return: json with the most recent time-series data
    """
    host = get_config()['host']
    token = get_access_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "timeSeriesName": time_series_names
    }

    if endpoint_id:
        params["endpointId"] = endpoint_id

    resp = requests.get(f'https://{host}/{SERVICE_NAME}/api/{API_VERSION}/applications/{app_name}/time-series/last',
                        params=params, headers=headers)
    resp.raise_for_status()

    return resp.json()

