import emeta

emeta.authenticate()
resp = emeta.get_query('2944', 'json')
print(resp)
