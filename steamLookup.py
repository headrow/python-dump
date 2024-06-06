import re
import requests
import steamConversions
import datetime
from datetime import timezone

key = ""

def customUrlToId(url: str):
    request = requests.get(f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={key}&vanityurl={url}")
    response = request.json()['response']
    success = response['success']

    if (success == 1):
        return ([success, response['steamid']])
    else:
        return ([success, response['message']])
    
def obtainAccountInfo(id: int):
    request = requests.get(f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={key}&steamids={id}")
    response = request.json()['response']['players']
    return (response)

def obtainAccountLevel(id: int):
    request = requests.get(f"https://api.steampowered.com/IPlayerService/GetSteamLevel/v1/?key={key}&steamid={id}")
    response = request.json()['response']

    if ('player_level' in response):
        return response['player_level']
    else:
        return 0
    
def obtainUsernameHistory(id: int):
    request = requests.get(f"https://steamcommunity.com/profiles/{id}/ajaxaliases")
    response = request.json()
    return response

def obtainAccountBans(id: int):
    request = requests.get(f"https://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key={key}&steamids={id}")
    response = request.json()['players'][0]
    return response

def isProfilePublic(value: int):
    if (value == 1):
        return "Private"
    else:
        return "Public"
    
def profileStatus(value: int):
    if (value == 0):
        return "Offline"
    elif (value == 1):
        return "Online"
    elif (value == 2):
        return "Busy"
    elif (value == 3):
        return "Away"
    elif (value == 4):
        return "Snooze"
    elif (value == 5):
        return "Looking to Trade"
    else:
        return "Looking to Play"
    
def createText(info: dict):
    message = f"```Username: {info['personaname']}\n"
    pastUsers = obtainUsernameHistory(info['steamid'])
    bans = obtainAccountBans(info['steamid'])

    if (len(pastUsers) > 1):
        message += "Past Usernames: "

        for user in pastUsers:
            if (user['newname'] != info['personaname']):
                message += f"{user['newname']} ; "

        message = message[:-3] + "\n"


    if ('timecreated' in info):
        date = datetime.datetime.fromtimestamp(info['timecreated'], tz = timezone.utc)

    if ('realname' in info):
        message += f"Real Name: {info['realname']}\n"

    if ('loccountrycode' in info):
        message += f"Country: {info['loccountrycode']}\n"

    message += f"Status: {profileStatus(info['personastate'])}\nProfile Visibility: {isProfilePublic(info['communityvisibilitystate'])}\nLevel: {obtainAccountLevel(info['steamid'])}\nSteam ID: {steamConversions.commid_to_steamid(info['steamid'])}\nSteam3: {steamConversions.commid_to_usteamid(info['steamid'])}\nCommunity ID: {info['steamid']}\n"
        
    if (info['profileurl'].startswith("https://steamcommunity.com/id/")):
        message += f"Custom URL: {info['profileurl'].replace("https://steamcommunity.com/id/", "")[:-1]}\n"

    message += f"Permanent URL: https://steamcommunity.com/profiles/{info['steamid']}\n"
        
    if ('timecreated' in info):
        message += f"Creation Date: {date.strftime('%d-%m-%Y')}\n"

    message += f"Community Banned: {bans['CommunityBanned']}\nTrade Banned: {bans['EconomyBan'] != "none"}\nVAC Bans: {bans['NumberOfVACBans']}\nGame Bans: {bans['NumberOfGameBans']}\nProfile Picture:```{info['avatarfull']}"

    return message
    
def getProfile(url: str):
    getAccountFromCustomUrl = customUrlToId(url)
    
    if (getAccountFromCustomUrl[0] == 1):
        return (createText(obtainAccountInfo(getAccountFromCustomUrl[1])[0]))
    elif (getAccountFromCustomUrl[0] == 42):
        if (url.isnumeric() and len(obtainAccountInfo(url)) > 0):
            return (createText(obtainAccountInfo(url)[0]))
        elif (re.match(r"STEAM_0:(0|1):\d+", url)):
            return (createText(obtainAccountInfo(steamConversions.steamid_to_commid(url))[0]))
        elif (re.match(r"\[U:1:\d+\]", url)):
            return(createText(obtainAccountInfo(steamConversions.usteamid_to_commid(url))[0]))
        else:
            return ("This account doesn't exist.")
    else:
        return(f"An error with the code {getAccountFromCustomUrl[0]} occurred with the following message: {getAccountFromCustomUrl[1]}.")