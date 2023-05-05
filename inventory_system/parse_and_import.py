import os
import sqlite3
import requests
import re

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

def fetch_and_parse_java_file():
    url = "https://raw.githubusercontent.com/tigartar/testserver/main/server-src/server/items/ItemTemplateCreator.java"
    response = requests.get(url)
    java_file = response.text

    pattern = r'createItemTemplate\((\d+),.*?name="([^"]+)"'
    item_data = re.findall(pattern, java_file, re.DOTALL)

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
    item_data = fetch_and_parse_java_file()
    import_items(item_data)
