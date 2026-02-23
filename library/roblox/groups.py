import requests

from library.core import console

RO_GROUP_API = "https://groups.roblox.com/v2/groups?groupIds={g_id}"
RO_USER_INFO_API = "https://users.roblox.com/v1/users/"
RO_GROUP_THUMBNAILS = "https://thumbnails.roblox.com/v1/groups/icons?groupIds={g_id}&size=420x420&format=Png"

def GetRoGroupInfo(Group_Id: int) -> dict | None:
    try:
        read = requests.get(RO_GROUP_API.format(g_id=Group_Id), timeout=5)
        read.raise_for_status()
        data = read.json()

        if not data or not data.get('data'):
            return None
        
        group_infos = data["data"][0]
        if not group_infos:
            return None
        
        read_2 = requests.get(RO_USER_INFO_API + str(group_infos.get('owner', {}).get('id')), timeout=5)
        read_2.raise_for_status()
        data_2 = read_2.json()

        if not data_2:
            return None
        
        owner_name = data_2.get('displayName', 'Roblox') or "Roblox"

        read_3 = requests.get(RO_GROUP_THUMBNAILS.format(g_id=Group_Id), timeout=5)
        read_3.raise_for_status()
        data_3 = read_3.json()

        if not data_3 or not data_3.get('data'):
            return None
        
        group_icon = data_3["data"][0].get(
            'imageUrl',
            'https://prayoadmii.neocities.org/Assets/CDN/dsbot-rblx-avatar-placeholder.png'
        ) or "https://prayoadmii.neocities.org/Assets/CDN/dsbot-rblx-avatar-placeholder.png"

        return {
            "id": group_infos.get('id'),
            "name": group_infos.get('name'),
            "description": group_infos.get('description'),
            "hasVBadge": group_infos.get('hasVerifiedBadge'),
            "owner": {
                "id": group_infos.get('owner', {}).get('id'),
                "name": owner_name
            },
            "icon": group_icon
        }

    except Exception as e:
        console.warn(f"Roblox Group Got Exception As: {e}")
        return None