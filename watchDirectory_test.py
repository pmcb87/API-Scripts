# This script will generate new files/append to static files to test Watch Directory event sources

from datetime import datetime
import random
import string

current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
file_path = 'test'
file_extention = '.json'

def append_line_to_file(file_path, line):
    # Generate a random string of length 6 to append to the filename.
    # Comment next two lines IF you want a static file
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    file_path = f"{file_path}_{random_string}{file_extention}"
    
    # Uncomment next line IF you want a static file
    # file_path = 'test.txt'
    
    with open(file_path, 'a') as file:
        file.write(current_timestamp + '\n')
append_line_to_file(file_path, current_timestamp)
