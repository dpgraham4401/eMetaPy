"""
Get user information
"""

import requests, json, os

def current_user():
    """Request current user info"""
    base_url = 'https://rcraquery.epa.gov/metabase'
    auth_url = base_url + '/api/user/current'
    id = os.getenv('META_TOKEN')
    meta_head = {'Content-Type': 'application/json',
                 'X-Metabase-Session': id}
    res = requests.get(auth_url, headers=meta_head)
    data = res.json()
    return data
