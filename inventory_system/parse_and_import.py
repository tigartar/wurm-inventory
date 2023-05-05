import os
import sys
import sqlite3
import re
import argparse

def parse_item_data(file_paths):
    item_data = []
    template_id_pattern = r'\d+|\w+'
    pattern = re.compile(r'createItemTemplate\(\s*(' + template_id_pattern + r')\s*,\s*"([^"]+)"\s*,\s*"([^"]+)"\s*,\s*"([^"]+)"\s*,\s*(\d+)\s*,\s*(\d+)\s*\);')

    for file_path in file_paths:
        with open(file_path, 'r') as file:
            content = file.read()
            matches = pattern.findall(content)
            item_data.extend(matches)

    # Filter out any non-numeric templateId values
    item_data = [item for item in item_data if item[0].isdigit()]

    return item_data

def create_inventory_db(item_data, output_file):
    conn = sqlite3.connect(output_file)
    cursor = conn.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS ITEMS (TEMPLATEID INT PRIMARY KEY, NAME TEXT, DESCRIPTION TEXT, MODELNAME TEXT, SIZE INT, WEIGHT REAL)')

    for item in item_data:
        template_id = int(item[0])
        name = str(item[1])
        description = str(item[2])
        model_name = str(item[3])
        size = int(item[4])
        weight = float(item[5])

        cursor.execute("INSERT INTO ITEMS (TEMPLATEID, NAME, DESCRIPTION, MODELNAME, SIZE, WEIGHT) VALUES (?, ?, ?, ?, ?, ?)",
                    (template_id, name, description, model_name, size, weight))

    conn.commit()
    conn.close()

def main():
    parser = argparse.ArgumentParser(description='Parse and import Wurm item data.')
    parser.add_argument('action', choices=['parse', 'import'], help='Action to perform: parse or import.')
    parser.add_argument('file', help='File to parse or SQLite database file to import data into.')
    args = parser.parse_args()

    if args.action == 'parse':
        file_paths = [args.file]
        item_data = parse_item_data(file_paths)
        for item in item_data:
            print(item)
    elif args.action == 'import':
        output_file = args.file
        item_data = parse_item_data(['Items.java'])
        create_inventory_db(item_data, output_file)

if __name__ == '__main__':
    main()
