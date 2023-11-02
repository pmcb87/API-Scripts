import json
from datetime import datetime, timedelta
import datetime
import logging
from logging.handlers import SysLogHandler
import requests

# Configure the logger to send logs to the syslog server
logger = logging.getLogger()
syslog_handler = SysLogHandler(address=('127.0.0.1', 514))
logger.addHandler(syslog_handler)
logger.setLevel(logging.INFO)

# This defines time range up to current time, delta can be modified to make the API call less frequently
current_timestamp = datetime.datetime.now(datetime.timezone.utc)
delta = timedelta(minutes=15)
start_search_date = current_timestamp - delta
timestamp_ms = int(start_search_date.timestamp())

# Action list available: https://api.slack.com/admins/audit-logs-call#actions
actions1 = 'user_login_failed, user_login, user_logout_compromised, user_logout_non_compliant_mobile_app_version, user_logout'
actions2 = 'more_actions, more_actions, more_actions'
actions3 = 'more_actions, more_actions, more_actions'

# Define the API endpoint and headers
url1 = (f'https://api.slack.com/audit/v1/logs?action={actions1}&oldest={timestamp_ms}')
url2 = (f'https://api.slack.com/audit/v1/logs?action={actions2}&oldest={timestamp_ms}')
url3 = (f'https://api.slack.com/audit/v1/logs?action={actions3}&oldest={timestamp_ms}')

headers = {
    'Authorization': 'Bearer ENTER-BEARER-TOKEN-HERE'
}

# Make the API call
# Slack Audit Log API documentation: https://api.slack.com/admins/audit-logs

# API Call with actions1
try:
    response = requests.get(url1, headers=headers)
    if response.status_code == 200:
        data = response.json()
        
        for item in data['entries']:
            # Convert the Unix timestamp to ISO format
            unix_timestamp = item['date_create']
            timestamp_datetime = datetime.datetime.fromtimestamp(unix_timestamp)
            iso_format_timestamp = timestamp_datetime.isoformat()
            
            # Update the 'date_create' field with the ISO format timestamp
            item['date_create'] = iso_format_timestamp
            
            # Log the updated JSON item
            json_string = json.dumps(item)
            logger.info(json_string)    
    else:
        # Log an error message to the syslog server
        logger.error(f'API call 1 failed with status code {response.status_code}: {response.text}')

except json.JSONDecodeError:
    # Log a JSON parsing error to the syslog server
    logger.error('Failed to parse JSON response from API call 1.')
    
    
# API Call with actions2

try:
    response = requests.get(url2, headers=headers)
    if response.status_code == 200:
        data = response.json()
        
        for item in data['entries']:
            # Convert the Unix timestamp to ISO format
            unix_timestamp = item['date_create']
            timestamp_datetime = datetime.datetime.fromtimestamp(unix_timestamp)
            iso_format_timestamp = timestamp_datetime.isoformat()
            
            # Update the 'date_create' field with the ISO format timestamp
            item['date_create'] = iso_format_timestamp
            
            # Log the updated JSON item
            json_string = json.dumps(item)
            logger.info(json_string)    
    else:
        # Log an error message to the syslog server
        logger.error(f'API call failed with status code {response.status_code}: {response.text}')

except json.JSONDecodeError:
    # Log a JSON parsing error to the syslog server
    logger.error('Failed to parse JSON response from the API.')


# API Call with actions3

try:
    response = requests.get(url3, headers=headers)
    if response.status_code == 200:
        data = response.json()
        
        for item in data['entries']:
            # Convert the Unix timestamp to ISO format
            unix_timestamp = item['date_create']
            timestamp_datetime = datetime.datetime.fromtimestamp(unix_timestamp)
            iso_format_timestamp = timestamp_datetime.isoformat()
            
            # Update the 'date_create' field with the ISO format timestamp
            item['date_create'] = iso_format_timestamp
            
            # Log the updated JSON item
            json_string = json.dumps(item)
            logger.info(json_string)    
    else:
        # Log an error message to the syslog server
        logger.error(f'API call 3 failed with status code {response.status_code}: {response.text}')

except json.JSONDecodeError:
    # Log a JSON parsing error to the syslog server
    logger.error('Failed to parse JSON response from API call 3.')
