import asyncio
import subprocess
import tempfile
import os
import uuid
import aiohttp
import botconfig as config
from library.core.helpmodule.randomtextcreator import GetRandomText

def get_video_duration(path: str) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            path
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    return float(result.stdout.strip())


async def ConvertToGif(DiscordAttachmentURL, OutputFileName="output.gif"):
    temp_path = os.path.join(
        tempfile.gettempdir(),
        config.BotOwnerTeam,
        config.AppName,
        "temporary",
        "gifcreator"
    )
    os.makedirs(
        temp_path,
        exist_ok=True
    )

    input_file = os.path.join(
        temp_path,
        f"tmp_{GetRandomText()}.mp4"
    )
    output_file = os.path.join(
        temp_path,
        OutputFileName
    )

    async with aiohttp.ClientSession() as session:
        async with session.get(DiscordAttachmentURL) as resp:
            if resp.status != 200:
                raise Exception("Failed to download attachment")

            with open(input_file, "wb") as f:
                f.write(await resp.read())

    duration = await asyncio.to_thread(
        get_video_duration,
        input_file
    )

    fps = 15
    if duration <= 5:
        fps = 15
    elif duration <= 10:
        fps = 10
    else:
        fps = 5

    command = [
        "ffmpeg",
        "-y",
        "-loglevel", "error",
        "-nostats",
        "-i",
        input_file,
        "-vf", f"fps={fps},scale=350:-1:flags=lanczos",
        "-loop", "0",
        output_file
    ]

    await asyncio.to_thread(
        subprocess.run,
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True
    )
    os.remove(input_file)

    return output_file