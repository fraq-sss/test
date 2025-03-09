from threading import Thread
from requests import post

DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1269430457863241758/r-GdE7ndNOOXelJnvK5e6-n1Zr1ENfinCrE_uTY7G4p7jsCV6FNkW1bmbCRx10mIE1Iw'

content = "connected"
kwargs = {'url': DISCORD_WEBHOOK_URL, 'json': {'content': content}}
Thread(target=post, kwargs=kwargs).start()
