# This script can be used to query for LDAP user and group information and write this data to a file.
# This is helpful to visualize the data in your domain to determine

import os
import json
from ldap3 import Server, Connection, ALL
from getpass import getpass

# When file reaches this size, a new one will be created
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Check if the file 'ldap_output_1.json' exists
if not os.path.exists('ldap_output_1.json'):
    with open('ldap_output_1.json', 'w') as file:
        pass

try:
    # Input LDAP Server below:
    server = Server('ldap://LDAP_SERVER_HERE:389', get_info=ALL)

    # Create a connection to the server with username and password hardcoded
    # Change user field but this must be in Down-Level Logon Name format as shown
    conn = Connection(server, user='DOMAIN\\user', password=('password')) 
    # Create a connection to the server which user is hardcoded but asks for password everytime this script is ran
    # conn = Connection(server, user='DOMAIN\\user', password=getpass('Enter your LDAP password: '))

    # Bind and start the connection
    if conn.bind():
        print('LDAP connection successful')

        # Perform the LDAP searches
        attributes_search1 = ['distinguishedName','userPrincipalName','givenName','sn','mail','proxyAddresses',
                              'title','department','manager','sAMAccountName','userAccountControl','whenCreated',
                              'whenChanged','pwdLastSet','mail','objectGUID','objectSid','memberOf']
        attributes_search2 = ['distinguishedName','description','whenCreated','whenChanged','member']

        searches = [
            ('CN=Users,DC=domain,DC=domain', '(objectClass=person)', attributes_search1),
            ('CN=Users,DC=domain,DC=domain', '(objectClass=group)', attributes_search2)
        ]

        entries = []

        # Iterate over the LDAP searches
        for search in searches:
            conn.search(search[0], search[1], attributes=search[2])
            for entry in conn.entries:
                entry_data = {}
                for attr in search[2]:
                    attr_value = getattr(entry, attr)
                    if isinstance(attr_value, list):
                        attr_value = [str(value) for value in attr_value]
                    else:
                        attr_value = str(attr_value)
                    entry_data[attr] = attr_value
                entries.append(entry_data)

        # Find the last file and determine the new file name
        i = 1
        while os.path.isfile(f'ldap_output_{i}.json') and os.path.getsize(f'ldap_output_{i}.json') > MAX_FILE_SIZE:
            i += 1

        new_file_name = f'ldap_output_{i}.json'

        # Write JSON data to the file with each entry on a new line
        with open(new_file_name, 'a') as file:
            for entry in entries:
                file.write(json.dumps(entry))
                file.write('\n')

        print('JSON data written to ' + new_file_name)

    else:
        print('LDAP connection failed')

except Exception as e:
    print(f'An error occurred: {str(e)}')

finally:
    # Unbind the connection
    conn.unbind()
