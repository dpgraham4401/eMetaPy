# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 09:56:44 2021

@author: dpgraham4401
"""

# import json
import os
import requests


def get_cards(card_type):
    """Request query (card) options"""
    base_url = 'https://rcraquery.epa.gov/metabase'
    auth_url = base_url + '/api/card'
    token_id = os.getenv('META_TOKEN')
    meta_head = {'Content-Type': 'application/json',
                 'X-Metabase-Session': token_id,
                 'f': card_type}
    res = requests.get(auth_url, headers=meta_head)
    res = res.json()
    return res


def get_card_id(card_id, export_frmt):
    """GET metabase card"""
    base_url = 'https://rcraquery.epa.gov/metabase'
    auth_url = base_url + '/api/card/' + card_id + '/query/' + export_frmt
    print(auth_url)
    token_id = os.getenv('META_TOKEN')
    meta_head = {'Content-Type': 'application/json',
                 'X-Metabase-Session': token_id}
    res = requests.post(auth_url, headers=meta_head)
    res = res.json()
    return res
