import rpc
import time
from time import mktime
import subprocess as sp
import re
import requests as req
from write import out

debugtoggle = True

client_id = '1032007391677521960'
rpc_obj = rpc.DiscordIpcClient.for_platform(client_id)


def updateData():
	global start_time
	start_time = mktime(time.localtime())
	cmd = "wmic process where name='robloxplayerbeta.exe' get /format:csv"
	res = sp.check_output(cmd)
	pattern = 'placeId=[0-9]+'
	match = re.search(pattern, str(res))
	global placeId, apiResp, thumbResp, placeName, placeThumb, placeBuilder
	placeId = match.group().split('=')[1]

	apiResp = req.get(f'https://www.roblox.com/places/api-get-details?assetId={placeId}').json()
	thumbResp = req.get(f'https://thumbnails.roblox.com/v1/places/gameicons?placeIds={placeId}&size=150x150&format=Png').json()

	placeName = apiResp.get('Name')
	placeThumb = thumbResp['data'][0].get('imageUrl') + ".png"
	placeBuilder = apiResp.get('Builder')

updateData()

if debugtoggle == True:
    out.debug(f"First Run PlaceID: {placeId}")
    out.debug(f"First Run Place Name: {placeName}")
    out.debug(f"First Run Place Thumbnail: {placeThumb}")
    out.debug(f"First Run Place Builder: {placeBuilder}")

while True:
    cmd = "wmic process where name='robloxplayerbeta.exe' get /format:csv"
    res = sp.check_output(cmd)
    pattern = 'placeId=[0-9]+'
    match = re.search(pattern, str(res))
    tempstore_placeId = match.group().split('=')[1]

    if tempstore_placeId != placeId:
        placeId = tempstore_placeId
        updateData()
        if debugtoggle == True:
                out.debug(f"Updated PlaceID: {placeId}")
                out.debug(f"Updated Place Name: {placeName}")
                out.debug(f"Updated Place Thumbnail: {placeThumb}")
                out.debug(f"Updated Place Builder: {placeBuilder}")

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
    time.sleep(5)
