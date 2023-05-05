import os
import re
import sqlite3
from glob import glob

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

def create_inventory_db(item_data, output_file):
    print("Creating inventory.db...")
    con = sqlite3.connect(output_file)
    cur = con.cursor()

    cur.execute('''CREATE TABLE items
                   (id INTEGER PRIMARY KEY, name TEXT NOT NULL)''')

    for item_id, item_name in item_data:
        cur.execute('''INSERT INTO items (id, name) VALUES (?, ?)''', (item_id, item_name))

    con.commit()
    con.close()

def main():
    local_folder = 'import'
    output_file = 'instance/inventory.db'

    item_data = fetch_and_parse_java_files(local_folder)
    create_inventory_db(item_data, output_file)

if __name__ == '__main__':
    main()
