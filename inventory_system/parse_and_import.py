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
                        item_data.append(values)

    return item_data

def create_inventory_db(item_data, output_file):
    if os.path.exists(output_file):
        print("The inventory.db file already exists. Skipping the creation process.")
        return

    conn = sqlite3.connect(output_file)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE ITEMS (
            TEMPLATEID INT,
            NAME VARCHAR (40),
            DESCRIPTION VARCHAR (256),
            PLACE SMALLINT,
            QUALITYLEVEL FLOAT,
            ORIGINALQUALITYLEVEL FLOAT,
            CAPACITY FLOAT,
            PARENTID BIGINT,
            LASTMAINTAINED BIGINT,
            CREATIONDATE BIGINT NOT NULL DEFAULT 0,
            CREATIONSTATE TINYINT NOT NULL DEFAULT 0,
            OWNERID BIGINT,
            LASTOWNERID BIGINT,
            TEMPERATURE SMALLINT,
            POSX FLOAT,
            POSY FLOAT,
            POSZ FLOAT,
            ROTATION FLOAT,
            ZONEID INT,
            DAMAGE FLOAT,
            SIZEX INT,
            SIZEY INT,
            SIZEZ INT,
            WEIGHT INT,
            MATERIAL TINYINT,
            LOCKID BIGINT,
            PRICE INT NOT NULL DEFAULT 0,
            BLESS TINYINT NOT NULL DEFAULT 0,
            ENCHANT TINYINT NOT NULL DEFAULT 0,
            BANKED TINYINT (1) NOT NULL DEFAULT 0,
            AUXDATA TINYINT NOT NULL DEFAULT 0,
            WORNARMOUR TINYINT (1) NOT NULL DEFAULT 0,
            REALTEMPLATE INT NOT NULL DEFAULT -10,
            COLOR INT NOT NULL DEFAULT -1,
            FEMALE TINYINT (1) NOT NULL DEFAULT 0,
            MAILED TINYINT (1) NOT NULL DEFAULT 0,
            MAILTIMES TINYINT NOT NULL DEFAULT 0,
            TRANSFERRED TINYINT (1) NOT NULL DEFAULT 0,
            CREATOR VARCHAR (40) NOT NULL DEFAULT "",
            HIDDEN TINYINT (1) NOT NULL DEFAULT 0,
            RARITY TINYINT NOT NULL DEFAULT 0,
            ONBRIDGE BIGINT NOT NULL DEFAULT -10,
            SETTINGS INT NOT NULL DEFAULT 0,
            COLOR2 INT NOT NULL DEFAULT -1,
            PLACEDONPARENT TINYINT (1) NOT NULL DEFAULT 0,
            PRIMARY KEY(TEMPLATEID)
        )
    ''')

    # Insert the item data into the ITEMS table
    for item in item_data:
        cursor.execute("INSERT INTO ITEMS (TEMPLATEID, NAME, DESCRIPTION, ...) VALUES (?, ?, ?, ...)", item)

    conn.commit()
    conn.close()
#   for item in item_data:
#        cursor.execute("INSERT OR IGNORE INTO inventory (id, name, weight, material) VALUES (?, ?, ?, ?)", item)
#
#    conn.commit()
#    conn.close()
    print("Inventory database created successfully.")



def main():
    local_folder = 'import'
    output_file = 'instance/inventory.db'

    item_data = fetch_and_parse_java_files(local_folder)
    create_inventory_db(item_data, output_file)

if __name__ == '__main__':
    main()
