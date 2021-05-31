"""
Request qeury  results?
"""

import requests, json, os

def get_cards(card_type):
    """Request query (card) options"""
    base_url = 'https://rcraquery.epa.gov/metabase'
    auth_url = base_url + '/api/card'
    id = os.getenv('META_TOKEN')
    meta_head = {'Content-Type': 'application/json',
                 'X-Metabase-Session': id,
                 'f': card_type}
    res = requests.get(auth_url, headers=meta_head)
    data = res.json()
    return data
