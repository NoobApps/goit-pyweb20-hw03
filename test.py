import os

for item in os.listdir('.venv'):
    item_path = os.path.join('.venv', item)
    if os.path.isfile(item_path):
        print(f"file: {item_path}")
    elif os.path.isdir(item_path):
        local_files = []
        for root, subdir, files in os.walk(item_path):
            for file in files:
                full_path = os.path.join(root, file)
                local_files.append(full_path)
            print(local_files)
        