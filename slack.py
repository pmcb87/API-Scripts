import json
from datetime import datetime, timedelta
import datetime
import logging
from logging.handlers import SysLogHandler
import requests

class JSONFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps(record.msg)

# Configure the logger to send logs to the syslog server
logger = logging.getLogger('slack_json')
syslog_handler = SysLogHandler(address=('127.0.0.1', 514))
logger.addHandler(syslog_handler)
logger.setLevel(logging.INFO)
syslog_handler.setFormatter(JSONFormatter())

# This defines time range up to current time, delta can be modified to make the API call less frequently
current_timestamp = datetime.datetime.now(datetime.timezone.utc)
delta = timedelta(minutes=15)
start_search_date = current_timestamp - delta
timestamp_ms = int(start_search_date.timestamp())

# Action list available: https://api.slack.com/admins/audit-logs-call#actions
actions = 'user_login_failed,user_login,user_logout_compromised,user_logout_non_compliant_mobile_app_version,user_logout,'

# Define the API endpoint and headers
url = (f'https://api.slack.com/audit/v1/logs?action={actions}&oldest={timestamp_ms}')
headers = {
    'Authorization': 'Bearer ENTER-BEARER-TOKEN-HERE'
    }

# Make the API call
# Slack Audit Log API documentation: https://api.slack.com/admins/audit-logs
try:
    response = requests.get(url, headers=headers)
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
