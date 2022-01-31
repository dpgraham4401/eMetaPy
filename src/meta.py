"""
meta.py
high level functionality related to pulling data from https://rcraquery.epa.gov
@author: dpgraham4401
"""

from conn.meta.auth import token
from conn.meta.query import query
from conn.meta.query import save_output


def run_meta(args):
    """Meta subcommand decision tree"""
    if args.auth:
        token()
    elif args.query:
        token()
        # res = query(args.query, args.output)
        res = query(args)
        if res.ok:
            if args.output:
                print("Saving data")
                save_output(res, args.output)
    else:
        token()
