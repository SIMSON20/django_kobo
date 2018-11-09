import requests
import json
from requests.auth import HTTPBasicAuth
import tablib

def get_kobo_data(connection, dataset_id):
    """
    Get data for Kobo form
    :param connection:
    :param dataset_id:
    :return:
    """
    host = connection.host_api.strip()
    auth_user = connection.auth_user.strip()
    auth_passwd = connection.auth_pass.strip()
    url = "{}/{}/{}?format=json".format(host, "data", str(dataset_id))
    r = requests.get(url, auth=HTTPBasicAuth(auth_user, auth_passwd))
    return json.loads(r.text)


def normalize_data(dataset):
    """
    Expects a list of dictionaries with key value pairs
    Returns a tablib dataset
    :param dataset:
    :return:
    """

    # make sure every row has the same keys.
    # get all unique keys
    keys = set()
    for row in dataset:
        keys |= set(row.keys())

    # add missing keys to rows
    for row in dataset:
        key_set = set(keys)
        key_set -= set(row.keys())
        for key in key_set:
            row[key] = None

    return tablib.Dataset().load(json.dumps(dataset, sort_keys=True))
