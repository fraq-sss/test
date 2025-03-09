import json
import urllib.request
from threading import Thread

DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1269430457863241758/r-GdE7ndNOOXelJnvK5e6-n1Zr1ENfinCrE_uTY7G4p7jsCV6FNkW1bmbCRx10mIE1Iw'

content = "connected"
data = json.dumps({'content': content}).encode('utf-8')

def send_webhook():
    req = urllib.request.Request(
        DISCORD_WEBHOOK_URL, 
        data=data, 
        headers={'Content-Type': 'application/json'}, 
        method='POST'
    )
    with urllib.request.urlopen(req) as response:
        response.read()

# Run in a separate thread
Thread(target=send_webhook).start()
