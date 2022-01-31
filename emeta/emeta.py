"""
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
    """
    Authenticate RCRAQuery account with username and password

    relies on a .env file in your HOME directory
    """
    try:
        if not os.getenv('META_TOKEN'):
            print("Token: no token present")
            if not os.path.exists("C:\\Users\\dgraha01\\.env"):
                __login()
            token_obj = __get_token()
            __write_token(token_obj)
        elif os.getenv('TOKEN_EXP'):
            current_time = datetime.now()
            current_time = current_time.isoformat()
            if os.getenv('TOKEN_EXP') < current_time:
                print("Token status: expired, retrieving new token")
                token_obj = __get_token()
                __write_token(token_obj)
            elif os.getenv('TOKEN_EXP') >= current_time:
                print("Token status: Good")
        else:
            print("Token error: hmm something ain't right contact support")
            sys.exit(1)
    except SystemExit as err:
        print(err)
        sys.exit(1)


def get_query(card_id, response_format, parameters=None):
    """
    Request query (card) options

    Args:
        card_id (str): Metabase query ID number in string format
        response_format (str): "json" or "csv"
        parameters (dict): dictionary with key values corresponding to metabase variable names
    """
    url_parameters = parse_params(parameters)
    endpoint = BASE_URL + '/api/card/' + card_id + '/query/' + response_format + url_parameters
    token_id = os.getenv('META_TOKEN')
    meta_head = {'Content-Type': 'application/json',
                 'X-Metabase-Session': token_id}
    res = requests.post(endpoint, headers=meta_head)
    if res.ok:
        res = res.json()[0]
        return res
    else:
        sys.exit(1)


def parse_params(parameters):
    """convert query parameters to payload"""
    # ToDo: remove url encoded hardcode so can handle multiple parameters
    if parameters is None:
        return ""
    else:
        for i in parameters:
            url_encoded_parameters = "?parameters=%5B%7B%22type%22%3A%22category%22%2C%22target%22%3A%5B%22variable%22%2C%5B%22temp" \
                "late-tag%22%2C%22" + i + "%22%5D%5D%2C%22value%22%3A%22" + parameters[i] + "%22%7D%5D"
        return url_encoded_parameters


def __login():
    os.environ['META_USER'] = input("Metabase username: ")
    os.environ['META_PASSWD'] = input("Metabase password: ")


def __get(end_point, header):
    """basic GET request currently no parameter options"""
    res = requests.get(end_point, headers=header)
    if res.ok:
        res = res.json()
        return res
    else:
        sys.exit(1)


def __post(end_point, post_data, header):
    """Basic POST Metabase endpoints"""
    res = requests.post(end_point, data=post_data, headers=header)
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
    meta_head = {'Content-Type': 'application/json'}
    res = __post(AUTH_URL, meta_data, meta_head)
    token_exp = datetime.now() + timedelta(days=EXPIRATION_DAYS)
    token_exp = token_exp.isoformat()
    token_obj = {'id': res['id'], 'exp': token_exp}
    os.environ['META_TOKEN'] = token_obj['id']
    os.environ['TOKEN_EXP'] = token_obj['exp']
    return token_obj


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
