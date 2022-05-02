import requests
import json
import os
import time

USER_ID = input("Twitch streamer username: ")
CLIENT_ID = ""
SECRET = ""

secretKeyURL = "https://id.twitch.tv/oauth2/token?client_id={}&client_secret={}&grant_type=client_credentials".format(CLIENT_ID, SECRET)
responseA = requests.post(secretKeyURL)
accessTokenData = responseA.json()

userIDURL = "https://api.twitch.tv/helix/users?login=%s"%USER_ID
responseB = requests.get(userIDURL, headers={"Client-ID":CLIENT_ID,
                                                'Authorization': "Bearer "+accessTokenData["access_token"]})
userID = responseB.json()["data"][0]["id"]

findVideoURL = "https://api.twitch.tv/helix/videos?user_id=%s"%userID
responseC= requests.get(findVideoURL, headers={"Client-ID":CLIENT_ID,
                                                'Authorization': "Bearer "+accessTokenData["access_token"]})
#print ( json.dumps( responseC.json(), indent = 4)  )

print("Found VODs:\n")

vodIDs = []

for vod in responseC.json()['data']:
    print("[" + vod['created_at'] + "]" + vod['id'] + " - " + vod['title'])
    vodIDs.append(vod['id'])


match input("Pick an action (A = all; S = selection; Q = quit):"):
    case "A":
        for vod in responseC.json()['data']:
            os.system("TwitchDownloaderCLI -m ChatDownload --id " + vod['id'] + " --timestamp-format Relative -o " + vod['id'] + ".txt")
    case "S":
        vodid = input("Enter VOD ID: ")
        os.system("TwitchDownloaderCLI -m ChatDownload --id " + vodid + " --timestamp-format Relative -o " + vodid + ".txt")
        while input("\nEnter VOD ID: ") in vodIDs:
            os.system("TwitchDownloaderCLI -m ChatDownload --id " + vodid + " --timestamp-format Relative -o " + vodid + ".txt")
    case "Q":
        exit

print("\nDone!")
os.system("pause")
