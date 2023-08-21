# This script's purpose is to return a report of all disabled users in IDR.
# It's important to note that IDR gathers this data from LDAP event sources. If your LDAP event sources are reporting incorrect data, this script will return the same incorrect data.

# Documentation of this API call can be found here: https://help.rapid7.com/insightidr/en-us/api/v1/docs.html#tag/Accounts/operation/searchAccounts

import requests
import json
from datetime import datetime

url1 = 'https://REGION.api.insight.rapid7.com/idr/v1/accounts/_search?size=1000' # Change region
headers1 = {
    'x-api-key': 'API KEY HERE',
    'Accept-version': 'strong-force-preview',
    'Content-Type': 'application/json'
}
# The body below can be modified using any of the search fields in the documentation
body = json.dumps({"search":[{"field": "disabled","operator": "EQUALS","value": True}],"sort":[{"field": "name","order": "ASC"}]})

# Generate current timestamp
timeStamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
filePath = f"disabled_users-" + timeStamp + ".json"

# Make API call
apiCall = requests.post(url1, headers=headers1, data=body)

if apiCall.status_code == 200:
    print('API call successful!')
    # Extract the values from the response
    response = apiCall.json()
    for item in response['data']:
        key1_1 = item.get('rrn')
        key2_1 = item.get('name')
        key3_1 = item.get('domain')
        key4_1 = item.get('disabled')
    
        # Prepare the key-value pairs as a dictionary
        kvps = {
            'rrn': key1_1,
            'name': key2_1,
            'domain': key3_1,
            'disabled': key4_1
        }

        # Convert the dictionary to JSON string
        json_string = json.dumps(kvps)
    
        # Write the JSON string to the log file
        with open(filePath, 'a') as file:
            file.write(json_string + '\n')
    print('Disabled users written to ' + filePath)

else:
    print('API call failed.')
    print('apiCall:', apiCall.status_code, apiCall.text)
