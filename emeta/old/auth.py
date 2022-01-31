"""
emeta.py
authorization for https://rcraquery.epa.gov
@author: dpgraham4401
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
    """logic for if new token needed and local storage"""
    try:
        if not os.getenv('META_TOKEN'):
            print("Token: no token present")
            if not os.path.exists('~/.env'):
                print("no ~/.env file found")
                os.environ['META_USER'] = input("Metabase username: ")
                os.environ['META_PASSWD'] = input("Metabase password: ")
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
                print("Token error: hmm something ain't right, "
                      "contact support")
    except SystemExit as err:
        print(err)
        sys.exit(1)


def __get_token():
    """Request new session token"""
    user = os.getenv('META_USER')
    passwd = os.getenv('META_PASSWD')
    meta_data = json.dumps({'username': user, 'password': passwd})
    meta_head = {'Content-Type': 'application/json'}
    res = requests.post(AUTH_URL, data=meta_data, headers=meta_head)
    data = res.json()

    token_exp = datetime.now() + timedelta(days=EXPIRATION_DAYS)
    token_exp = token_exp.isoformat()
    token_obj = {'id': data['id'], 'exp': token_exp}
    os.environ['META_TOKEN'] = token_obj['id']
    os.environ['TOKEN_EXP'] = token_obj['exp']
    return token_obj


def __write_token(token_obj):
    try:
        metabase_token_file = os.environ['HOME'] + "/.env"
        file = open(metabase_token_file, "w")
        file.write("\n")
        file.write("META_TOKEN=" + token_obj['id'] + '\n')
        file.write("TOKEN_EXP=" + token_obj['exp'])
        file.close()
    except IOError as err:
        print(err)
        sys.exit("IOError: could not write to .env")
