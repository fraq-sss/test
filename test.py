import http.client
import json

webhook_url = "discord.com"
webhook_path = "/api/webhooks/1311648949878128660/9zRG2MjsqIp5UFK3dso_eRrRYPLtZawspUevsPl4l9EdG44FhPIBidU4k2AYCRywteIK"

message = {
    "content": "Hello, this is a message from http.client!"
}

conn = http.client.HTTPSConnection(webhook_url)

json_message = json.dumps(message)

headers = {
    'Content-Type': 'application/json'
}

conn.request("POST", webhook_path, body=json_message, headers=headers)

response = conn.getresponse()
conn.close()
