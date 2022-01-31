# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 09:56:44 2021

@author: dpgraham4401
"""
import requests


class MetaRequest:
    """Request wrapper for rcraquery"""

    def __init__(self, base_url, token_id):
        self.base_url = base_url
        self.token_id = token_id

    def get(self, end_point):
        """
        basic GET request currently no pararmeter options
        """
        auth_url = self.base_url + end_point
        meta_head = {'Content-Type': 'application/json',
                     'X-Metabase-Session': self.token_id}
        res = requests.get(auth_url, headers=meta_head)
        res = res.json()
        return res

    def post(self, end_point, card_type):
        """
        Basic POST Metabase endpoints
        """
        auth_url = self.base_url + end_point
        meta_head = {'Content-Type': 'application/json',
                     'X-Metabase-Session': self.token_id,
                     'f': card_type}
        res = requests.get(auth_url, headers=meta_head)
        res = res.json()
        return res
