import requests

from library.core import console

GAME_ICON = "https://thumbnails.roblox.com/v1/games/icons?universeIds={universe_id}&size=512x512&format=Png"
UNIVERSE_FROM_PLACE = "https://apis.roblox.com/universes/v1/places/{place_id}/universe"
GAME_DATA = "https://games.roblox.com/v1/games?universeIds={universe_id}"
GAME_LIKES = "https://games.roblox.com/v1/games/votes?universeIds={universe_id}"
GAME_THUMBNAILS = "https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds={universe_id}&countPerUniverse=1&defaults=true&size=768x432&format=Png&isCircular=false"

def vote_percentage(up: int, down: int) -> float:
    total = up + down
    if total == 0:
        return 0.0
    return round((up / total) * 100, 2)

def resolve_universe_id(id: int) -> int | None:
    try:
        r = requests.get(UNIVERSE_FROM_PLACE.format(place_id=id))
        r.raise_for_status()
        data = r.json()

        if "universeId" in data:
            return data["universeId"]
    except Exception as e:
        console.warn(f"There Are Some Error While Freshing Thumbnails As: {e}")
        pass
    try:
        r = requests.get(GAME_DATA.format(universe_id=id))
        r.raise_for_status()
        data = r.json()

        if "data" in data and len(data["data"]) > 0:
            return id
    except Exception as e:
        console.warn(f"There Are Some Error While Freshing Thumbnails As: {e}")
        pass

    return None

def GetGameInfoAsync(id: int) -> dict:
    thumbnail_url = "https://prayoadmii.neocities.org/Assets/CDN/dsbot-rblx-place-thumb-placeholder.png"
    icon_url = "https://prayoadmii.neocities.org/Assets/CDN/dsbot-rblx-place-placeholder.png"
    upvote_count = 0
    downvote_count = 0

    universe_id = resolve_universe_id(id)
    if not universe_id:
        universe_id = id
    try:
        r = requests.get(GAME_DATA.format(universe_id=universe_id), timeout=5)
        r.raise_for_status()
        data = r.json()

        if "data" not in data or not data["data"]:
            return {"error": "There Are No Game Data Found!"}

        game = data["data"][0]

        try:
            r_thumb = requests.get(GAME_THUMBNAILS.format(universe_id=universe_id), timeout=5)
            r_thumb.raise_for_status()
            thumb_data = r_thumb.json()

            if "data" in thumb_data and len(thumb_data["data"]) > 0:
                thumbnails_list = thumb_data["data"][0].get('thumbnails', [])

                if thumbnails_list:
                    thumbnail_url = thumbnails_list[0].get('imageUrl')
        except Exception as e:
            console.warn(f"There Are Some Error While Freshing Game Thumbnails As: {e}")

        try:
            r_icon = requests.get(GAME_ICON.format(universe_id=universe_id), timeout=5)
            r_icon.raise_for_status()
            icon_data = r_icon.json()

            icon_url = icon_data["data"][0]["imageUrl"]
        except Exception as e:
            console.warn(f"There Are Some Error While Freshing Game Icons As: {e}")

        try:
            r_likes = requests.get(GAME_LIKES.format(universe_id=universe_id), timeout=5)
            r_likes.raise_for_status()
            likes_data = r_likes.json()

            upvote_count = likes_data["data"][0]["upVotes"]
            downvote_count = likes_data["data"][0]["downVotes"]
        except Exception as e:
            console.warn(f"There Are Some Error While Freshing Game Likes As: {e}")

        clean_data = {
            "universeId": game.get('id'),
            "rootPlaceId": game.get('rootPlaceId'),
            "name": game.get('name'),
            "description": game.get('description'),
            "creator": {
                "id": game.get('creator', {}).get('id'),
                "name": game.get('creator', {}).get('name'),
                "type": game.get('creator', {}).get('type')
            },
            "visits": game.get('visits'),
            "favorites": game.get('favoritedCount'),
            "maxPlayers": game.get('maxPlayers'),
            "playing": game.get('playing'),
            "thumbnail": thumbnail_url,
            "icon": icon_url,
            "votes": {
                "up": upvote_count,
                "down": downvote_count,
                "percent": vote_percentage(upvote_count, downvote_count)
            }
        }

        return clean_data
    
    except Exception as e:
        console.warn(f"There Are Some Error While Freshing Game Data As: {e}")
        return {"error": str(e)}