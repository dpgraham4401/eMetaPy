"""
query.py
pulling data from https://rcraquery.epa.gov
@author: dpgraham4401
"""

import os
import sys
import requests
import json

BASE_URL = 'https://rcraquery.epa.gov/metabase'


def get_export_fmt(output_path):
    """determine is json or csv format"""
    if 'csv' in output_path:
        return 'csv'
    elif 'json' in output_path:
        return 'json'
    else:
        print("ERROR: expected file type .json or .csv, received -->", output_path)
        sys.exit(1)


def save_output(result, output_path):
    """write to file"""
    out_format = get_export_fmt(output_path)
    if out_format == "json":
        result = result.json()
        with open(output_path, "w") as f:
            json.dump(result, f)
    elif out_format == "csv":
        with open(output_path, "w") as csv_file:
            csv_file.write(result.text)


def set_query_headers():
    token_id = os.getenv("META_TOKEN")
    meta_head = {'Content-Type': 'application/json',
                 'X-Metabase-Session': token_id}
    return meta_head


# def parse_params(args):
#     """convert CLI parameters to payload"""
#     # ToDo: remove url encoded hardcode
#     if args.parameter:
#         if len(args.parameter.split('=')) == 2:
#             metabase_var = args.parameter.split('=')
#             params = "?parameters=%5B%7B%22type%22%3A%22category%22%2C%22target%22%3A%5B%22variable%22%2C%5B%22temp" \
#                 "late-tag%22%2C%22" + metabase_var[0] + "%22%5D%5D%2C%22value%22%3A%22" + metabase_var[1] + "%22%7D%5D"
#         else:
#             params = ""
#         return params
#     else:
#         params = ""
#         return params


# def query(args):
#     """GET metabase card"""
#     card_id = args.query
#     output_path = args.output
#     meta_head = set_query_headers()
#     out_format = get_export_fmt(output_path)
#     params = parse_params(args)
#     query_url = BASE_URL + "/api/card/" + card_id + "/query/" + out_format + params
#     resp = requests.post(query_url, headers=meta_head)
#     return resp
