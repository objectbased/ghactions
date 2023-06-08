import os
import re

def scan_and_replace(directory):
    pattern = r'\${{\s*splunk\.secret\.key\s*}}'
    key_pattern = r'(?<=\${{\s*splunk\.secret\.key\s*}}\s*=\s*).*'
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith(".conf"):
                file_path = os.path.join(root, file_name)
                if os.path.isfile(file_path):
                    with open(file_path, 'r+') as file:
                        content = file.read()
                        match = re.search(pattern, content)
                        if match:
                            key_match = re.search(key_pattern, match.group(0))
                            if key_match:
                                key = key_match.group(0)
                                updated_content = re.sub(pattern, f"found ({key})", content)
                                file.seek(0)
                                file.write(updated_content)
                                file.truncate()
                                print(f"Processed: {file_path}")
                            else:
                                print(f"No key found in: {file_path}")
                        else:
                            print(f"No match found in: {file_path}")

# Usage example
directory_path = '/path/to/parent/directory'
scan_and_replace(directory_path)
