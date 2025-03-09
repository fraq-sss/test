import json
import urllib.request
import ba
ba.screenmessage("^^")

# Replace with your Discord webhook URL
webhook_url = "https://discord.com/api/webhooks/1305806260796653569/XAo0-lE0pXL38Bu2rulRXh-raihDsg3LJT9gQYzVbSoiB6yXmPw2s0pMAcrrCEl_-tLz"

# The message to send
message = {
    "content": "Hello!"
}

# Convert the message to JSON
data = json.dumps(message).encode('utf-8')

# Create the request
request = urllib.request.Request(
    webhook_url, 
    data=data, 
    headers={"Content-Type": "application/json"},
    method="POST"
)

# Send the request
with urllib.request.urlopen(request) as response:
    # Read the response (optional)
    response_data = response.read()
    print("Message sent successfully:", response_data)
