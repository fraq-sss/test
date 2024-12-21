import json
import urllib
#import ba

u = "https://discord.com/api/webhooks/1314158911267536936/k3Q9W4xp5L1kLTOwGMXAzlwQepVScbrt60hamaK50ivfswiRgHhieJreY1pNWCRJ-hew"
d = json.dumps({"content": "Hello, Discord!"})#.encode("utf-8")
r = urllib.request.Request(u, data=d, headers={"Content-Type": "application/json"})
with urllib.request.urlopen(r) as s:
  pass
