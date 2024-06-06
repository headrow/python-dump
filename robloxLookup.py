import requests
import datetime
from datetime import datetime

def getIdFromUser(username: str):
    request = requests.post("https://users.roblox.com/v1/usernames/users", json = {
        "usernames": [
            username
        ],
        "excludeBannedUsers": False
    })

    response = request.json()["data"]

    if (len(response) > 0):
        return response[0]["id"]
    else:
        return "This account doesn't exist."
    
def getBasicUserInfo(id: int):
    request = requests.get(f"https://users.roblox.com/v1/users/{id}")
    response = request.json()

    if ('errors' in response):
        return ([False, response['errors'][0]])
    else:
        return ([True, response])
    
def getAvatarThumbnail(id: int):
    request = requests.get(f"https://thumbnails.roblox.com/v1/users/avatar?userIds={id}&size=720x720&format=Png&isCircular=false")
    response = request.json()['data'][0]

    if (response['state'] != "Completed"):
        return ([False, response['state']])
    else:
        return ([True, response['imageUrl']])
    
def getLastOnline(id: int):
    request = requests.post("https://presence.roblox.com/v1/presence/last-online", json = {
        "userIds": [
            id
        ]
    })

    response = request.json()['lastOnlineTimestamps'][0]['lastOnline']
    return response

def checkDate(id: int):
    request = requests.get(f"https://inventory.roblox.com/v2/users/{id}/inventory/8?limit=100&sortOrder=Asc")
    response = request.json()

    if ('errors' in response):
        return ([False, ""])
    else:
        nextPage = response['nextPageCursor']
        data = response['data']
        date = None

        while (date == None):
            for i in range(len(data)):
                print(data[i]['assetId'])
                if (data[i]['assetId'] == 102611803):
                    date = datetime.strptime(data[i]['created'][:10], "%Y-%m-%d")
                    break

            if (date == None):
                request = requests.get(f"https://inventory.roblox.com/v2/users/{id}/inventory/8?limit=100&cursor={nextPage}&sortOrder=Asc")
                response = request.json()
                nextPage = response['nextPageCursor']
                data = response['data']
        
        return ([True, date])

def isVerified(id: int):
    request = requests.get(f"https://inventory.roblox.com/v1/users/{id}/items/0/102611803/is-owned")
    response = request.json()

    if (response == True):
        date = checkDate(id)

        if (date[0] == False):
            return response
        else:
            return f"{response} ({date[1].strftime('%d-%m-%Y')})"
    else:
        return response
    
def createText(info: dict):
    avatar = getAvatarThumbnail(info['id'])
    joinDate = datetime.strptime(info['created'][:10], "%Y-%m-%d")
    lastOnline = datetime.strptime(getLastOnline(info['id'])[:10], "%Y-%m-%d")
    message = f"```Username: {info['name']}\nDisplay Name: {info['displayName']}\nUser ID: {info['id']}\nJoin Date: {joinDate.strftime('%d-%m-%Y')}\nLast Online: {lastOnline.strftime('%d-%m-%Y')}"
    
    if (info['isBanned'] == False):
        message += f"\nEmail Verified: {isVerified(info['id'])}"

    message += f"\nTerminated: {info['isBanned']}\nVerified Badge: {info['hasVerifiedBadge']}"

    if (len(info['description']) > 0):
        message += f"\nDescription:\n\"{info['description']}\""

    message += f"\nAvatar: "

    if (avatar[0] == True):
        message += f"```{avatar[1]}"
    else:
        message += f"{avatar[1]}```"

    return message

def getProfile(option: str, url: str):
    profileId: int

    if (option == "user"):
        profileId = getIdFromUser(url)
    elif (option == "id"):
        profileId = url
    else:
        return "You need to type a valid option."
    
    userInfo = getBasicUserInfo(profileId)

    if (userInfo[0] == False):
        if (userInfo[1]['code'] == 3):
            return "This account doesn't exist."
        else:
            return f"An error with the code {userInfo[1]['code']} occurred with the following message: {userInfo[1]['message']}."
    else:
        return createText(userInfo[1])