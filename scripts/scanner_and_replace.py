import os

def scan_and_replace(directory):
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith(".conf"):
                file_path = os.path.join(root, file_name)
                if os.path.isfile(file_path):
                    with open(file_path, 'r+') as file:
                        content = file.read()
                        updated_content = content.replace("${{ variable }}", "found")
                        file.seek(0)
                        file.write(updated_content)
                        file.truncate()
                    print(f"Processed: {file_path}")

# Usage example
directory_path = '/path/to/parent/directory'
scan_and_replace(directory_path)
