# eMeta
### library for using the metabase apis at RCRAQuery.epa.gov
These are functions that I had duplicated in many places at work

## environment variables
- META_USER - rcraquery user name (used if META_TOKEN and META_EXP are missing or expired)
- META_PASSWD - rcraquery password (used if META_TOKEN and META_EXP are missing or expired)
- META_TOKEN - auth token received from metabse
- META_EXP - expiration date of token in iso format
  - example: 2022-02-12T14:31:58.122010



```Python
import emeta

os.getenv('META_USER')
os.getenv('META_PASSWD')

emeta.authenticate()

# get the query id number from the url 
# I removed ability to download as CSV for now, maybe in future
# parameters is a dict with the keys set to the specified query's varaible names
parameters= {"GEN_ID_VAR": "TXR000040923",
             "TSDF_ID_VAR": "TXD000719518"}
resp = emeta.get_query('2944', 'json', parameters
```
