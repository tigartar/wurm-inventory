import sqlite3
import requests
import re

def create_table():
    conn = sqlite3.connect('inventory.db')
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
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    for item in item_data:
        item_id, item_name = item
        c.execute('INSERT OR REPLACE INTO items (id, name) VALUES (?, ?)', (item_id, item_name))

    conn.commit()  # Add this line to commit the changes to the database
    conn.close()

if __name__ == "__main__":
    create_table()
    item_data = fetch_and_parse_java_file()
    import_items(item_data)
