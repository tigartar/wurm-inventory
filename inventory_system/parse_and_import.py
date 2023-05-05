import os
import re
import sqlite3
import sys

def fetch_and_parse_java_files(input_folder):
    item_data = []

    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.java'):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    content = f.read()
                    matches = re.findall('createItemTemplate\((.*?)\);', content, re.DOTALL)
                    for match in matches:
                        values = [value.strip() for value in match.split(',')]
                        item_data.append(values[:6])  # Assuming the first 6 values correspond to the columns in the table

    return item_data

def create_inventory_db(item_data, output_file):
    conn = sqlite3.connect(output_file)
    cursor = conn.cursor()

    # Create the ITEMS table
    cursor.execute('''CREATE TABLE IF NOT EXISTS ITEMS (
                        TEMPLATEID INTEGER PRIMARY KEY,
                        NAME TEXT,
                        DESCRIPTION TEXT,
                        MODELNAME TEXT,
                        SIZE INTEGER,
                        WEIGHT REAL
                      )''')

    # Insert the item data into the ITEMS table
    for item in item_data:
        # Convert the values to the appropriate data types
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


if __name__ == "__main__":
    input_folder = sys.argv[1]
    output_file = sys.argv[2]

    item_data = fetch_and_parse_java_files(input_folder)
    create_inventory_db(item_data, output_file)
