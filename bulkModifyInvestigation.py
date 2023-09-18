# The purpose of this script is to allow modifying investigations en masse. 
# This script is not supported by Rapid7 and its behavior may change or break without warning.
# There are no timeout parameters in this script so beware of the API Rate Limiting limits. 

import json
from datetime import datetime, timedelta
import datetime
import requests
import sys

# Report Parameters
file_path = 'bulkInvestigationReport'
file_extension = '.txt'

# Time Parameters
current_timestamp = datetime.datetime.now(datetime.timezone.utc)
number_of_closed = 1
gathered_investigations = []
delta = timedelta(days=390) # This range can be modified per your requirements. Max = 390 Days.
thirteen_months = current_timestamp - delta
start_date = thirteen_months.strftime('%Y-%m-%d'+ 'T' + '%H:%M:%S' + 'Z')
end_date = current_timestamp.strftime('%Y-%m-%d'+ 'T' + '%H:%M:%S' + 'Z')

# print('Investigation search start date: ' + str(start_date))
# print('Investigation search end date: ' + str(end_date))

# Search Parameters
region = 'REGION CODE HERE'
api_key = 'API KEY HERE'
page = 1
base_url = f'https://{region}.api.insight.rapid7.com/'
endpoint1 = 'idr/v2/investigations/_search'
endpoint2 = 'idr/v2/investigations/'

headers = {
    'x-api-key': f'{api_key}',
    'Accept-version': 'investigations-preview',
    'Content-Type': 'application/json'
}

# The body of the API POST can be modified to change the search which returns the investigations.
# Please refer to this documentation for more information: https://help.rapid7.com/insightidr/en-us/api/v2/docs.html#tag/Investigations/operation/searchInvestigations

body = json.dumps({
    "end_time": str(end_date),
    "search": [
        {
            "field": "title",
            "operator": "CONTAINS",
            "value": ""
        },
        {
            "field": "status",
            "operator": "EQUALS",
            "value": "OPEN"
        }
    ],
    "sort": [
        {
            "field": "created_time",
            "order": "ASC"
        }
    ],
    "start_time": str(start_date)
}, indent = 4)

def getInvestigationList():
    global page
    global rrn_list
    rrn_list = []
    
    iterator = True
    while iterator:
        gi_call = requests.post(base_url + endpoint1, headers=headers, 
                                params=({
                                'index': page - 1}
                                        ), data = body
        )
        # print (gi_call.text)
        gi_data = gi_call.json()
        metadata = gi_data.get('metadata', {})
        index = metadata.get('index')
        # size = metadata.get('size')
        total_data = metadata.get('total_data')
        total_pages = metadata.get('total_pages')
        if total_data == 0:
            print ('No investigations found')
            print ('Exiting...')
            sys.exit(0)
        elif index == 0:
            print (f'{total_data} investigations found')
            print (f'{total_pages} number of pages found')
        
        if gi_call.status_code == 200:
            # Add Investigation info to lists
            for item in gi_data['data']:
                global rrn
                rrn = item.get('rrn')
                title = item.get('title')
                created_time = item.get('created_time')
                investigation_info = {
                    'rrn': rrn,
                    'title': title,
                    'created_time': created_time
                }
                investigationEntry = json.dumps(investigation_info)
                gathered_investigations.append(investigationEntry + '\n')
                rrn_list.append(rrn)
                # closeInvestigation()
        if page == total_pages:
            iterator = False
            print('There are ' + str(sum(1 for item in rrn_list if isinstance(item,str))) + ' investigations in the gathered list')
            modifyList()
            break
        else:
            page += 1

def modifyList():
    for i in rrn_list:
        global number_of_closed
        global action
        action = json.dumps({
            'status': 'OPEN'
            })
        ci_call = requests.request("PATCH", base_url + endpoint2 + i, headers=headers, data=action)
        if ci_call.status_code == 200:
            number_of_closed += 1
            global closed_rrn
            closed_rrn = []
            closed_rrn.append(rrn)
        elif ci_call.status_code == 202:
            print(str(ci_call.status_code) + ': That is unexpected...')
        else:
            print(str(ci_call.status_code) + ': Failed to modify ' + rrn)
    reportQuestion()

def reportOpt_1():
    print('Creating Report...')
    createReport()

def reportOpt_2():
    print('You chose to not make a report, script will exit.')
    sys.exit(0)

def reportQuestion():
    user_choice = input('Would you like to print a report? Y/n : ')
    if user_choice.lower() == 'y':
        reportOpt_1()
    elif user_choice == '':
        reportOpt_1()
    elif user_choice.lower() == 'n':
        reportOpt_2()
    else:
        print('Invalid choice. Please select a valid option.')

def createReport():
    global file_path
    r_timestamp = current_timestamp.strftime("%Y-%m-%d %H:%M:%S")
    file_path = f"{file_path}_{r_timestamp}{file_extension}"
    
    with open(file_path, 'a') as file:
        file.write('API Script ran' + str(r_timestamp) + '\n')
        global action
        
        file.write(str(number_of_closed) + ' investigations modified \n')
        file.write('API parameters: \n')
        file.write('Action taken: ' + action + '\n')
        file.write(body + '\n')
        global gathered_investigations        
        for i in gathered_investigations:
            file.write(i + '\n')
    print('Report made: ' + file_path)

getInvestigationList()
