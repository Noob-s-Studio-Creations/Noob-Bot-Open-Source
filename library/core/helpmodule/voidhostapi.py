import requests

import botconfig as config

from library.core import console

headers = {
  "Authorization": f"Bearer {str(config.Void_Host_API_Key)}",
  "Accept": "Application/vnd.pterodactyl.v1+json",
  "Content-Type": "application/json"
}

def byte_to_mib(byte: float) -> float:
    return byte / (1024 ** 2)

def GetVoidServerResources():
    try:
        response = requests.get(
            f"https://panel.voidhosting.vip/api/client/servers/{config.VHServerID}/resources",
            headers=headers,
            timeout=5
        )
        response.raise_for_status()
    except requests.RequestException as e:
        console.warn(f"VoidHosting API Error As: {e}")
        return None, None

    data = response.json()

    return data

def GetVoidServerInfos():
    try:
        response = requests.get(
            f"https://panel.voidhosting.vip/api/client/servers/{config.VHServerID}",
            headers=headers,
            timeout=5
        )
        response.raise_for_status()
    except requests.RequestException as e:
        console.warn(f"VoidHosting API Error As: {e}")
        return None, None

    data = response.json()

    return data

def GetVoidServerCompleteData():
    UnE_Usage = GetVoidServerResources()
    UnE_Limit = GetVoidServerInfos()

    if not UnE_Usage or not UnE_Limit:
        return None

    Usage = UnE_Usage["attributes"]["resources"]
    Limit = UnE_Limit["attributes"]["limits"]

    mem_limit = Limit.get('memory', 0)
    disk_limit = Limit.get('disk', 0)

    if mem_limit <= 0 or disk_limit <= 0:
        return None

    mem_percent = (byte_to_mib(Usage.get('memory_bytes', 0)) / mem_limit) * 100
    disk_percent = (byte_to_mib(Usage.get('disk_bytes', 0)) / disk_limit) * 100

    return {
        "memory": round(mem_percent, 2),
        "disk": round(disk_percent, 2)
    }