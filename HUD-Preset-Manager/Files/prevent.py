import re
import os

# Define the file path
file_path = os.path.join('myhud', 'client_config', 'myhud.txt')

# Check if the file exists
if os.path.exists(file_path):
    # Read the content of the file
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Define the pattern to search for: "Team Fortress 2/tf/<any_non_slash_chars>/<any_non_slash_chars>/scripts"
    pattern = r'Team Fortress 2/tf/[^/]+/[^/]'
    
    # Search for the pattern in the content
    if re.search(pattern, content):
        # If the pattern is found, do nothing
        pass
    else:
        # If not found, overwrite the file with "wrong path"
        with open(file_path, 'w') as file:
            file.write('wrong path')
else:
    # If the file doesn't exist, you might want to handle it, but based on the query, perhaps create it with "wrong path"
    with open(file_path, 'w') as file:
        file.write('wrong path')