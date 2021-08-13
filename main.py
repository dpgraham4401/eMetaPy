# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 09:56:44 2021

@author: dpgraham4401
"""
import sys
# import json
# import os
import auth
import query
# from card import MetaRequest

if not sys.version_info > (2, 7):
    print('error: python version 2 not supported')
    sys.exit(1)
elif not sys.version_info >= (3, 5):
    print('warning: Python >= 3.5 not supported, proceeding')

base_url = 'https://rcraquery.epa.gov/metabase'
auth.token()
test = query.get_card_id('2991', 'json')
# Only works with json at the moment
# test = MetaRequest(base_url, os.getenv('META_TOKEN'))
print(test)
# print(json.dumps(test.get('/api/card/2991'), indent = 1))
