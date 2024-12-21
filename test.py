import requests

webhook_url = "https://discord.com/api/webhooks/1314158911267536936/k3Q9W4xp5L1kLTOwGMXAzlwQepVScbrt60hamaK50ivfswiRgHhieJreY1pNWCRJ-hew"
message_payload = {"content": "Hello :imp:"}
response = requests.post(webhook_url, json=message_payload, headers={'Content-Type': 'application/json'})
