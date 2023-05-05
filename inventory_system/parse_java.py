import requests
import javalang

def download_java_file(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to download the file: {response.status_code}")

def parse_java_file(java_code):
    tree = javalang.parse.parse(java_code)
    class_name = tree.types[0].name
    return class_name

if __name__ == "__main__":
    url = "https://raw.githubusercontent.com/tigartar/testserver/main/server-src/server/items/ItemTemplateCreator.java"
    java_code = download_java_file(url)
    class_name = parse_java_file(java_code)
    print(f"Class name: {class_name}")
