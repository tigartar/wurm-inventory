import os
import sqlite3
import re

def parse_java_files(import_folder):
    item_data_list = []

    for filename in os.listdir(import_folder):
        if filename.endswith('.java'):
            with open(os.path.join(import_folder, filename), 'r') as file:
                content = file.read()
                item_data = extract_item_data(content)
                if item_data:
                    item_data_list.append(item_data)
    return item_data_list

def extract_item_data(content):
    # You can modify the regex pattern to match the fields in your .java files
    pattern = re.compile(r'final int templateId = (.*?);.*?final int size = (.*?);.*?final String name = (.*?);.*?final String plural = (.*?);.*?final String itemDescriptionSuperb = (.*?);.*?final String itemDescriptionNormal = (.*?);.*?final String itemDescriptionBad = (.*?);.*?final String itemDescriptionRotten = (.*?);.*?final String itemDescriptionLong = (.*?);.*?final short\[\] itemTypes = (.*?);.*?final short imageNumber = (.*?);.*?final short behaviourType = (.*?);.*?final int combatDamage = (.*?);.*?final long decayTime = (.*?);.*?final int centimetersX = (.*?);.*?final int centimetersY = (.*?);.*?final int centimetersZ = (.*?);.*?final int primarySkill = (.*?);.*?final byte\[\] bodySpaces = (.*?);.*?final String modelName = (.*?);.*?final float difficulty = (.*?);.*?final int weightGrams = (.*?);.*?final byte material = (.*?);.*?final int value = (.*?);.*?final boolean isPurchased = (.*?);', re.DOTALL)
    match = re.search(pattern, content)
    if match:
        return match.groups()
    return None

def create_database_and_table(instance_folder):
    db_path = os.path.join(instance_folder, 'inventory.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items
        (templateId INTEGER, size INTEGER, name TEXT, plural TEXT, itemDescriptionSuperb TEXT, itemDescriptionNormal TEXT, itemDescriptionBad TEXT, itemDescriptionRotten TEXT, itemDescriptionLong TEXT, itemTypes TEXT, imageNumber INTEGER, behaviourType INTEGER, combatDamage INTEGER, decayTime INTEGER, centimetersX INTEGER, centimetersY INTEGER, centimetersZ INTEGER, primarySkill INTEGER, bodySpaces TEXT, modelName TEXT, difficulty REAL, weightGrams INTEGER, material INTEGER, value INTEGER, isPurchased BOOLEAN)
    """)
    conn.commit()

    return conn, cursor

def insert_item_data_to_database(conn, cursor, item_data_list):
    for item_data in item_data_list:
        cursor.execute("""
            INSERT INTO items (templateId, size, name, plural, itemDescriptionSuperb, itemDescriptionNormal, itemDescriptionBad, itemDescriptionRotten, itemDescriptionLong, itemTypes, imageNumber, behaviourType, combatDamage, decayTime, centimetersX, centimetersY, centimetersZ, primarySkill, bodySpaces, modelName, difficulty, weightGrams, material, value, isPurchased)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, item_data)
    conn.commit()

def main():
    import_folder = 'import'
    instance_folder = 'instance'

    item_data_list = parse_java_files(import_folder)

    conn, cursor = create_database_and_table(instance_folder)

    insert_item_data_to_database(conn, cursor, item_data_list)

    conn.close()

if __name__ == '__main__':
    main()
