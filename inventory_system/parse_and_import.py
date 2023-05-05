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

            pattern = r'(?<=\.)createItemTemplate\((\d+),\s*"([^"]+)",[^,]*,[^,]*,[^,]*,[^,]*,[^,]*,[^,]*,[^,]*,[^,]*,[^,]*,[^,]*,[^,]*,([^,]*),([^,]*),'
            for match in re.finditer(pattern, java_text, re.DOTALL):
                item_data.append((match.group(1), match.group(2), float(match.group(3)), int(match.group(4))))

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
