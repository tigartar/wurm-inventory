import os
import sqlite3
import requests
import re
from glob import glob

# Define the path to the instance folder
instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')

# Define the path to the inventory.db file inside the instance folder
db_path = os.path.join(instance_path, 'inventory.db')

def create_table():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT)''')
    conn.commit()
    conn.close()

def fetch_and_parse_java_files(folder_url):
    # Download the file list from the folder containing the Java files
    file_list_response = requests.get(folder_url)
    file_list = file_list_response.text.split('\n')

    item_data = []

    for file_name in file_list:
        if not file_name.strip():
            continue

        file_url = f"{folder_url}/{file_name}"
        response = requests.get(file_url)
        java_file = response.text

        pattern = r'createItemTemplate\((\d+),.*?name="([^"]+)"'
        file_item_data = re.findall(pattern, java_file, re.DOTALL)
        item_data.extend(file_item_data)

    return item_data

def import_items(item_data):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    for item in item_data:
        item_id, item_name = item
        c.execute('INSERT OR REPLACE INTO items (id, name) VALUES (?, ?)', (item_id, item_name))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_table()

    # Replace this URL with the URL of the folder containing the Java files
    folder_url = "https://github.com/tigartar/wurm-inventory/tree/main/inventory_system/Import"
    item_data = fetch_and_parse_java_files(folder_url)
    import_items(item_data)
