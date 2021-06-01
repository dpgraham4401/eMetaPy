'''
Test use of the MetaBase API
'''

import sys
import json
import auth
#import user
import query

if not sys.version_info > (2, 7):
    print('error: python version 2 not supported')
    sys.exit(1)
elif not sys.version_info >= (3, 5):
    print('warning: Python >= 3.5 not supported, proceeding')

auth.token()
test = query.get_card_id('2991', 'json')
print(json.dumps(test, indent = 1))
