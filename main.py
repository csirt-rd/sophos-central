from elasticsearch import Elasticsearch
import siem
import ssl
import json


# Sophos script to read the logs thorugh the sophos central api.
# Creates log-file at .\log\result.txt with many single json objects seperated with empty lines
# Saves state at .\state\siem_lastrun_events.obj
siem.main()

# Read .\log\result.txt
with open('log/result.txt', 'r') as file:
    filecontent = file.read()

# Split content from .\log\result.txt to a list of json objects
doc = filecontent.split('\n')

# Prepare connection to elasticsearch
context = ssl.create_default_context()
## Loads default certs from host os
context.load_default_certs()
es = Elasticsearch(['kibana.abr4x.com:9200'], http_auth=('oencarnacion', 'Liz2172!'),
                   scheme="https", port=443, ssl_context=context)

# handle every single entry and commits it to elasticsearch
for entry in doc:
    ## drops empty entries
    if(entry != ""):
        body = json.loads(entry)
        res = es.index("sophos-1", id=body['id'], body=body)
        print(res['result'])

# Deleting result.txt is required, else old entries would be submitted again
# Error that result.txt is still open in this script, delete it in transfer_log.bat
print("finished")
