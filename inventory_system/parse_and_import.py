import re
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import Item

def fetch_and_parse_java_file():
    url = "https://raw.githubusercontent.com/tigartar/testserver/main/server-src/server/items/ItemTemplateCreator.java"
    response = requests.get(url)
    java_file = response.text

    pattern = r'createItemTemplate\((\d+),.*?name="([^"]+)"'
    item_data = re.findall(pattern, java_file, re.DOTALL)

    return item_data
	
def import_items_to_db(item_data):
    engine = create_engine('sqlite:///inventory.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    for item_id, item_name in item_data:
        item = Item(id=int(item_id), name=item_name)
        session.add(item)

    session.commit()
    session.close()

if __name__ == '__main__':
    item_data = fetch_and_parse_java_file()
    import_items_to_db(item_data)
