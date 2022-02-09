"""
100+ lines of the worst code I've ever written, but whatever it's working for now
Library of functions for using metabase API available at RCRAQuery.epa.gov
"""
from datetime import datetime, timedelta
import os
import sys
import json
import requests

BASE_URL = 'https://rcraquery.epa.gov/metabase'
AUTH_URL = BASE_URL + '/api/session'
EXPIRATION_DAYS = 12


def authenticate():
    """Authenticate RCRAQuery account with username and password in runtime environment"""
    token_exist = __check_token_exists()
    if token_exist:
        token_fresh = __check_token_expiration()
        if not token_fresh:
            login_exist = __check_login_exist()
            if login_exist:
                new_token = __get_token()
                __set_environment_variables(new_token)
            else:
                print("Token expired and META_USER or META_PASSWD environment variables not found")
                sys.exit(1)


def __check_token_exists():
    if os.getenv("META_TOKEN"):
        return bool(os.getenv("META_EXP"))
    else:
        return False


def __check_token_expiration():
    if os.getenv('META_EXP'):
        current_time = datetime.now().isoformat()
        return bool(os.getenv('META_EXP') > current_time)
    else:
        return False


def __check_login_exist():
    if os.getenv("META_USER"):
        return bool(os.getenv("META_PASSWD"))
    else:
        return False


def get_query(card_id, response_format, parameters=None):
    """
    Request query (card) options

    Args:
        card_id (str): Metabase query ID number in string format
        response_format (str): "json" or "csv"
        parameters (dict): dictionary with key values corresponding to metabase variable names
    """
    url_parameters = __parse_params(parameters)
    endpoint = BASE_URL + '/api/card/' + card_id + '/query/' + response_format + url_parameters
    token_id = os.getenv('META_TOKEN')
    meta_head = {'Content-Type': 'application/json',
                 'X-Metabase-Session': token_id}
    res = requests.post(endpoint, headers=meta_head)
    if res.ok:
        res = res.json()
        return res
    else:
        sys.exit(1)


def __parse_params(parameters):
    """convert query parameters to payload"""
    # ToDo: remove url encoded hardcode so can handle multiple parameters
    if parameters is None:
        return ""
    else:
        for i in parameters:
            return "?parameters=%5B%7B%22type%22%3A%22category%22%2C%22target%22%3A%5B%22variable%22%2C%5B%22temp" \
                                     "late-tag%22%2C%22" + i + "%22%5D%5D%2C%22value%22%3A%22" + parameters[
                                         i] + "%22%7D%5D"


def __get(end_point):
    """basic GET request currently no parameter options"""
    meta_head = {'Content-Type': 'application/json'}
    res = requests.get(end_point, headers=meta_head)
    if res.ok:
        res = res.json()
        return res
    else:
        sys.exit(1)


def __post(end_point, post_data):
    """Basic POST Metabase endpoints"""
    meta_head = {'Content-Type': 'application/json'}
    res = requests.post(end_point, data=post_data, headers=meta_head)
    if res.ok:
        res = res.json()
        return res
    else:
        sys.exit(1)


def __get_token():
    """Request new session token"""
    user = os.getenv('META_USER')
    passwd = os.getenv('META_PASSWD')
    meta_data = json.dumps({'username': user, 'password': passwd})
    res = __post(AUTH_URL, meta_data)
    token_exp = datetime.now() + timedelta(days=EXPIRATION_DAYS)
    token_exp = token_exp.isoformat()
    token_obj = {'id': res['id'], 'exp': token_exp}
    return token_obj


def __set_environment_variables(token_object):
    os.environ['META_TOKEN'] = token_object['id']
    os.environ['TOKEN_EXP'] = token_object['exp']


def __write_token(token_obj):
    try:
        metabase_token_file = "C:\\Users\\dgraha01\\.env"
        file = open(metabase_token_file, "w")
        file.write("\n")
        file.write("META_TOKEN=" + token_obj['id'] + '\n')
        file.write("TOKEN_EXP=" + token_obj['exp'])
        file.close()
    except IOError as err:
        print(err)
        sys.exit("IOError: could not write to .env")
