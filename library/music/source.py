import yt_dlp
import asyncio
import discord

from library.core import console
from library.core import servertype

ytdlp_default_search = "scsearch"

if servertype.get_platform() == "win" or servertype.get_platform() == "rpi":
    ytdlp_default_search = "ytsearch"
else:
    ytdlp_default_search = "scsearch"

YTDL_OPTIONS = {
    "format": "bestaudio[ext=webm]/bestaudio/best",
    "quiet": True,
    "default_search": ytdlp_default_search,
    "noplaylist": False,
    "source_address": "0.0.0.0",
    "extract_flat": "in_playlist",
    "js_runtimes": {
        "node": {}
    },
    "extractor_args": {
        "youtube": {
            "player_client": [
                "android"
            ]
        }
    }
}

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn -protocol_whitelist file,http,https,tcp,tls,crypto,pipe"
}

ytdl = yt_dlp.YoutubeDL(YTDL_OPTIONS)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data):
        super().__init__(source, volume=1.0)
        self.title = data.get('title', 'Unknown Title')
        self.web_url = data.get('webpage_url')

    @classmethod
    async def extract(cls, query: str):
        loop = asyncio.get_running_loop()

        data = await loop.run_in_executor(
            None,
            lambda: ytdl.extract_info(query, download=False)
        )

        if not data:
            raise ValueError("yt-dlp Returned No Data")

        if "entries" in data:
            return [e for e in data["entries"] if e]

        return [data]

    @classmethod
    async def create(cls, query: str):
        loop = asyncio.get_running_loop()

        try:
            data = await loop.run_in_executor(
                None,
                lambda: ytdl.extract_info(
                    query,
                    download=False
                )
            )
        except Exception as e:
            console.error(f"yt-dlp Extract Failed: {e}")
            raise

        if not data:
            raise ValueError("yt-dlp Returned No Data")
        
        if "entries" in data:
            raise ValueError("create() Received Playlist Data")

        if not data:
            raise ValueError("No Valid Entry Found")

        stream_url = data.get('url')
        if not stream_url:
            raise ValueError("No Stream URL Found")

        return cls(
            discord.FFmpegPCMAudio(
                stream_url,
                executable="ffmpeg",
                **FFMPEG_OPTIONS
            ),
            data=data
        )