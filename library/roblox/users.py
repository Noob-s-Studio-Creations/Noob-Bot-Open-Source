import requests

from library.core import console

RO_USER_SEARCH_API = "https://users.roblox.com/v1/users/search"
RO_USER_INFO_API = "https://users.roblox.com/v1/users/"
RO_THUMBNAILS_API = "https://thumbnails.roblox.com/v1/users/avatar-headshot"

def GetUserByUsernameAsync(username: str) -> dict | None:
    try:
        res = requests.get(RO_USER_SEARCH_API, params={"keyword": username, "limit": 10}, headers={"accept": "application/json"}, timeout=10)

        if res.status_code != 200:
            console.warn(f"Roblox User Search Failed: {res.status_code}")
            return None, res.status_code

        users = res.json().get('data', [])
        matched_user = next(iter(users), None)

        if not matched_user:
            return None, None

        user_id = matched_user["id"]

        info_res = requests.get(RO_USER_INFO_API + str(user_id), timeout=10)

        if info_res.status_code != 200:
            console.warn(f"Get User Info Failed For: {user_id}")
            return None, info_res.status_code

        user_info = info_res.json()

        pfp_res = requests.get(RO_THUMBNAILS_API, params={"userIds": user_id, "size": "420x420", "format": "Png", "isCircular": "false"}, timeout=10)

        pfp_url = None
        if pfp_res.status_code == 200:
            pfp_data = pfp_res.json().get('data', [])
            if pfp_data:
                pfp_url = pfp_data[0].get('imageUrl')

        return {
            "id": user_id,
            "name": user_info.get('name'),
            "display_name": user_info.get('displayName'),
            "description": user_info.get('description'),
            "banned": user_info.get('isBanned'),
            "hasVerifiedBadge": matched_user.get('hasVerifiedBadge'),
            "profile_picture": pfp_url
        }, None

    except Exception as e:
        console.error(f"Roblox User Info Exception As: {e}")
        return None, None
