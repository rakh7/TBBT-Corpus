
import json
import re
import collections

episodeList = []
Listing = {}

with open("episode_links.json","r") as fhandle:
    episodeList = json.load(fhandle)
    fhandle.close()

for link in episodeList:
    info = link.split("/")[-2]
    more_info = info.split("-")
    season = more_info[1]
    episode = more_info[3]
    title = " ".join(more_info[4:])
    if int(season) not in Listing:
        Listing[int(season)] = []
    Listing[int(season)].append((int(episode),title,link))

with open("temp.json","w") as fhandle:
    json.dump(Listing,fhandle,indent=4)
    fhandle.close()