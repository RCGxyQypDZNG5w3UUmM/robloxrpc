import rpc
import time
from time import mktime
import subprocess as sp
import re
import requests as req

client_id = '1032007391677521960'
rpc_obj = rpc.DiscordIpcClient.for_platform(client_id)
print("RPC connection successful.")

cmd = "wmic process where name='robloxplayerbeta.exe' get /format:csv"

res = sp.check_output(cmd)

pattern = 'placeId=[0-9]+'
match = re.search(pattern, str(res))
placeId = match.group().split('=')[1]

api_resp = req.get(f'https://www.roblox.com/places/api-get-details?assetId={placeId}').json()
thumb_resp = req.get(f'https://thumbnails.roblox.com/v1/places/gameicons?placeIds={placeId}&size=150x150&format=Png').json()

placeName = api_resp.get('Name')
placeThumb = thumb_resp['data'][0].get('imageUrl') + ".png"
placeBuilder = api_resp.get('Builder')

time.sleep(5)
start_time = mktime(time.localtime())
while True:
	activity = {
            "state": f"by {placeBuilder}",
            "details": f"{placeName}",
            "timestamps": {
                "start": start_time
            },
            "assets": {
                "large_image": placeThumb,
                "large_text": placeId
            }
        }
	rpc_obj.set_activity(activity)
	time.sleep(15)
