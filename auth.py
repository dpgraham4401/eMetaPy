'''
Manage Metabase session token
'''
from datetime import datetime, timedelta
import requests, json, os
#from typing import ForwardRef
from dotenv import load_dotenv
#from requests.api import get

load_dotenv()

def get_token():
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
    token = {'id': data['id'], 'exp': token_exp}
    os.environ['META_TOKEN'] = token['id']
    os.environ['TOKEN_EXP'] = token['exp']
    return token

def set_token():
    """logic for if new token needed and local storage"""
    try:
        f = open(".env")
        f.close()
    except IOError:
        print("IOError: dot env file not found")
    try:
        if not os.getenv('META_TOKEN'):
            print('Set Token: no token present, retireving')
            token = get_token()
            f = open(".env", "a")
            f.write("\nMETA_TOKEN=" + token['id'] + '\n')
            f.write("TOKEN_EXP=" + token['exp'])
            f.close()
        elif os.getenv('TOKEN_EXP'):
            current_time = datetime.now()
            current_time = current_time.isoformat()
            if os.getenv('TOKEN_EXP') < current_time:
                print('Set Token: expired, retrieving new token')
                token = get_token()
                f = open(".env", "a")
                f.write("\nMETA_TOKEN=" + token['id'] + '\n')
                f.write("TOKEN_EXP=" + token['exp'])
            elif os.getenv('TOKEN_EXP') >= current_time:
                print('Set Token: not expired, continuing')
            else:
                print('Set Token: error_1, hmmm something aint right, '
                'contact support ')
    except Exception as e:
        print(e)
