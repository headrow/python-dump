# pasted from here https://gist.github.com/bcahue/4eae86ae1d10364bb66d

steamid64ident = 76561197960265728

# community id to steam id
def commid_to_steamid(commid):
    steamid = []
    steamid.append('STEAM_0:')
    steamidacct = int(commid) - steamid64ident
    
    if steamidacct % 2 == 0:
        steamid.append('0:')
    else:
        steamid.append('1:')
    
    steamid.append(str(steamidacct // 2))
    
    return ''.join(steamid)

# steam id to community id
def steamid_to_commid(steamid):
    sid_split = steamid.split(':')
    commid = int(sid_split[2]) * 2
    
    if sid_split[1] == '1':
        commid += 1
    
    commid += steamid64ident
    return commid

# steam id to steam3
def steamid_to_usteamid(steamid):
    steamid_split = steamid.split(':')
    usteamid = []
    usteamid.append('[U:1:')
    
    y = int(steamid_split[1])
    z = int(steamid_split[2])
    
    steamacct = z * 2 + y
    
    usteamid.append(str(steamacct) + ']')
    
    return ''.join(usteamid)

# community id to steam3
def commid_to_usteamid(commid):
    usteamid = []
    usteamid.append('[U:1:')
    steamidacct = int(commid) - steamid64ident
    
    usteamid.append(str(steamidacct) + ']')
    
    return ''.join(usteamid)

# steam3 to steam id
def usteamid_to_steamid(usteamid):
    for ch in ['[', ']']:
        if ch in usteamid:
            usteamid = usteamid.replace(ch, '')
    
    usteamid_split = usteamid.split(':')
    steamid = []
    steamid.append('STEAM_0:')
    
    z = int(usteamid_split[2])
    
    if z % 2 == 0:
        steamid.append('0:')
    else:
        steamid.append('1:')

    steamacct = z // 2
    
    steamid.append(str(steamacct))
    
    return ''.join(steamid)

# steam3 to community id
def usteamid_to_commid(usteamid):
    for ch in ['[', ']']:
        if ch in usteamid:
            usteamid = usteamid.replace(ch, '')
    
    usteamid_split = usteamid.split(':')
    commid = int(usteamid_split[2]) + steamid64ident
    
    return commid