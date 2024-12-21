
import json
import urllib.request
import urllib.parse

webhook_url = "https://discord.com/api/webhooks/1314158911267536936/k3Q9W4xp5L1kLTOwGMXAzlwQepVScbrt60hamaK50ivfswiRgHhieJreY1pNWCRJ-hew"  # Replace with your webhook URL
message = "Hello from Python!"

data = {
    "content": message
}

# Encode the data as JSON
data = json.dumps(data).encode("utf-8")

# Create the request
req = urllib.request.Request(webhook_url, data=data, headers={
    "Content-Type": "application/json"
})

# Send the request
response = urllib.request.urlopen(req)

print(response.read().decode("utf-8"))
