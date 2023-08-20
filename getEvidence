import requests
import json
import datetime
import time
import os

# This script will make a call to list the last 15 Minutes of investigations using search parameters then use the gathered Investigation IDs to retrieve the evidence for those investigations and append this information to a log file.
# This could be modified to upload to a ticketing application. Just replace lines 72-92 with the API POST call to whatever application you would like.

# When file reaches this size, a new one will be created
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# This retrieves the timestamps from when this script is ran and subtracts 15 minutes for the start and endtime parameters in the first API call. Modify this as necessary.
iso_timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
# Convert to a datetime object
end_time = datetime.datetime.fromisoformat(iso_timestamp)
start_time = end_time - datetime.timedelta(minutes=15) # change hours value as necessary

# Convert the both datetimes to an ISO timestamp and format it per API requirements
end_time = end_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-4] + 'Z'
start_time_f = start_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-4] + 'Z'

# Public Documentation for this API call: https://help.rapid7.com/insightidr/en-us/api/v2/docs.html#tag/Investigations/operation/searchInvestigations
url1 = 'https://REGION.api.insight.rapid7.com/idr/v2/investigations/_search?size=50' # Update Region
headers1 = {
    'x-api-key': 'API-KEY', # Enter ORG API KEY
    'Accept-version': 'investigations-preview',
    'Content-Type': 'application/json',
}
search_params='{"end_time": "' + end_time + '", "sort": [{"field": "created_time","order": "ASC" }], "start_time": "' + start_time_f + '"}'
payload1 = {
    'rrn': 'rrn',
    'title': 'title',
    'created_time': 'created_time',
    'priority': 'priority'
}

url2base = 'https://REGION.api.insight.rapid7.com/idr/v1/restricted/investigations/' # Update Region
headers2 = {
    'x-api-key': 'API-KEY', # Enter ORG API KEY
    'Accept-version': 'investigations-preview',
    'Content-Type': 'application/json'
}
# Make the first API call
response1 = requests.post(url1, headers=headers1, json=payload1, data=search_params)
if response1.status_code == 200:
    print('Search Investigations API call successful')
    data1 = response1.json()
    for item in data1['data']:
        # Extract the desired values from the first response
        key1_1 = item.get('rrn')
        key2_1 = item.get('created_time')
        key3_1 = item.get('priority')
        # Update the URL or payload for Get Evidence API call
        url2 = url2base + key1_1 + '/evidence'
        # Make the second API call
        response2 = requests.get(url2, headers=headers2)
        if response2.status_code == 200:
            print('Get Evidence API call successful')
            # Extract keys and values from the second response
            data2 = response2.json()
            key1_2 = data2['indicator_occurrences']
            # Prepare the key-value pairs as a dictionary
            kvps = {
                'rrn': key1_1,
                'created_time': key2_1,
                'priority': key3_1,
                'evidence': key1_2
            }            
            # Convert the dictionary to JSON string
            json_string = json.dumps(kvps)
            filepath = 'ie_1.json'
            if not os.path.exists(filepath):
                with open(filepath, "w") as file:
                    pass
            # Find the last file and determine filesize
            i = 1
            while os.path.isfile(f'ie_{i}.json') and os.path.getsize(f'ie_{i}.json') > MAX_FILE_SIZE:
                i += 1
            new_filepath = f'ie_{i}.json'
            while os.path.isfile(new_filepath) and os.path.getsize(new_filepath) > MAX_FILE_SIZE:
                i += 1
                new_filepath = f'ie_{i}.json'
            
            # Read the existing data file
            with open(new_filepath, 'r') as file:
                existing_data = file.read()
                
            # Check if the JSON string already exists in the data file
            with open(new_filepath, 'a') as file:
                if json_string + '\n' not in existing_data:
                # Append the JSON string to the data file
                    with open(new_filepath, 'a') as file:
                        file.write(json_string + '\n')
                        print('Investigation & Evidence appended to the data file.')
                else:
                    print('Investigation & Evidence already exists in the data file.')
                url2 = url2base
        else:
            print('Get Evidence API call failed.')
            print('Response2:', response2.status_code, response2.text)
else:
    print('Search Investigations API call failed.')
    print('Response1:', response1.status_code, response1.text)
