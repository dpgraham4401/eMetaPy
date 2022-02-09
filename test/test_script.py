import emeta

emeta.authenticate()
# resp = emeta.get_query('2944', 'json')
# print(resp)

parameter = {"GEN_ID_VAR": "TXR000040923"}
resp = emeta.get_query('2944', 'json', parameter)
print(resp)