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

def fetch_and_parse_java_files(local_folder):
    print("Fetching and parsing Java files...")
    item_data = []

    for java_file_path in glob(os.path.join(local_folder, '*.java')):
        with open(java_file_path, 'r', encoding='utf-8') as java_file:
            java_text = java_file.read()

            pattern = r'createItemTemplate\((\d+),.*?name="([^"]+)"'
            file_item_data = re.findall(pattern, java_text, re.DOTALL)
            item_data.extend(file_item_data)

    return item_data



def import_items(item_data):
    print("Importing items into the database...")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    for item in item_data:
        item_id, item_name = item
        c.execute('INSERT OR REPLACE INTO items (id, name) VALUES (?, ?)', (item_id, item_name))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    print("Creating table in the database...")
    create_table()

    # Replace this URL with the URL of the folder containing the Java files
    local_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "import")
    item_data = fetch_and_parse_java_files(local_folder)
    import_items(item_data)
