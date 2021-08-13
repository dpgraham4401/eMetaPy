# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 09:45:41 2021

@author: dpgraham4401
"""
from datetime import datetime, timedelta
import os
import sys
import json
import requests
from dotenv import load_dotenv
# from requests.api import get

load_dotenv()


def token():
    """logic for if new token needed and local storage"""
    try:
        file = open(".env")
        file.close()
    except IOError as err:
        print(err)
        sys.exit("'.env' file with credentials cannot be opened")
    try:
        if not os.getenv('META_TOKEN'):
            print("Token: no token present, retireving")
            token_obj = __get_token()
            __write_token(token_obj)
        elif os.getenv('TOKEN_EXP'):
            current_time = datetime.now()
            current_time = current_time.isoformat()
            if os.getenv('TOKEN_EXP') < current_time:
                print("Token: expired, retrieving new token")
                token_obj = __get_token()
                __write_token(token_obj)
            elif os.getenv('TOKEN_EXP') >= current_time:
                print("Token: Good")
            else:
                print("Token error: hmmm something ain't right, "
                      "contact support")
    except SystemExit as err:
        print(err)
        sys.exit(1)


def __get_token():
    """Request new session token"""
    base_url = 'https://rcraquery.epa.gov/metabase'
    auth_url = base_url + '/api/session'
    user = os.getenv('META_USER')
    passwd = os.getenv('META_PASSWD')
    meta_data = json.dumps({'username': user, 'password': passwd})
    meta_head = {'Content-Type': 'application/json'}
    res = requests.post(auth_url, data=meta_data, headers=meta_head)
    data = res.json()

    token_exp = datetime.now() + timedelta(days=12)
    token_exp = token_exp.isoformat()
    token_obj = {'id': data['id'], 'exp': token_exp}
    os.environ['META_TOKEN'] = token_obj['id']
    os.environ['TOKEN_EXP'] = token_obj['exp']
    return token_obj


def __write_token(token_obj):
    try:
        file = open(".env", "a")
        file.write("\nMETA_TOKEN=" + token_obj['id'] + '\n')
        file.write("TOKEN_EXP=" + token_obj['exp'])
        file.close()
    except IOError as err:
        print(err)
        sys.exit("IOError: could not write to .env")
