import discord
import asyncio

from library.music.queue import SongQueue
from library.music.source import YTDLSource
from library.core import console

class MusicPlayer:
    def __init__(self, guild, bot):
        self.guild = guild
        self.bot = bot
        self.queue = SongQueue()
        self.voice: discord.VoiceClient | None = None
        self.current = None
        self.text_channel = None
        self.next_song_event = asyncio.Event()
        self.player_task: asyncio.Task | None = None

    async def connect(self, channel: discord.VoiceChannel):
        if not self.voice or not self.voice.is_connected():
            self.voice = await channel.connect()

            await channel.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)

            console.info(f"Connected To {channel.name} In {self.guild.name}")

            if not self.player_task:
                self.player_task = asyncio.create_task(self.player_loop())

    async def disconnect(self):
        if self.voice:
            channel = self.voice.channel
            channel_name = channel.name if channel else "Unknown"

            if self.voice.is_playing() or self.voice.is_paused():
                self.voice.stop()
            
            channel_name = self.voice.channel.name if self.voice else "Unknown"

            if channel:
                try:
                    await channel.edit(status=None, reason="Reset Status When Bot Leave!")
                except Exception as e:
                    pass

            await self.voice.disconnect(force=True)

            console.info(f"Disconnected From {channel_name} In {self.guild.name}")

            self.queue.loop_mode = "1"
            self.voice = None
        
        await self.queue.clear()

        self.current_query = None

        if self.player_task:
            self.player_task.cancel()
            self.player_task = None
        
        self.next_song_event = asyncio.Event()

    async def add_song(self, query: str):
        try:
            entries = await YTDLSource.extract(query)

            added = 0
            for entry in entries:
                url = entry.get("webpage_url") or entry.get("url")
                if not url:
                    continue

                await self.queue.put(url)
                added += 1

            console.log(f"Added {str(added)} Track(s) To Queue In {self.guild.name}")
            return f"{str(added)} Track(s)"

        except Exception as e:
            console.warn(f"Error Adding Song Or Playlist As: {e}")
            return 0

    async def player_loop(self):
        try:
            while True:
                self.next_song_event.clear()
                query = await self.queue.get() 

                if not self.voice or not self.voice.is_connected():
                    continue

                self.current_query = query
                try:
                    song = await YTDLSource.create(query)
                except Exception as e:
                    console.error(f"Failed To Create Music Source As: {e}")
                    continue

                if not self.voice or not self.voice.is_connected():
                    continue

                self.voice.play(song, after=lambda e: self.bot.loop.call_soon_threadsafe(self.after_song, e))

                if self.text_channel:
                    try:
                        if self.queue.loop_mode != "2":
                            await self.text_channel.send(f"Now I'm Playing: **{song.title}**", silent=True)
                    except Exception as e:
                        console.warn(f'Cannot Sent "Now Playing" Message During An Error As {e}')
                    try:
                        await self.voice.channel.edit(status=f'Noob Bot Was Playing "{song.title}" Here!', reason=f"Update The Playing Music For {str(self.voice.channel.name)}")
                    except Exception as e:
                        console.warn(f'Cannot Edit "Now Playing" Voice Status During An Error As {e}')
                
                await self.next_song_event.wait()
        except asyncio.CancelledError:
            console.info(f"Player Loop Was Cancelled!")

    def after_song(self, error):
        if error:
            console.error(f"Music Player Error As: {error}")

            if self.text_channel:
                asyncio.run_coroutine_threadsafe(self.text_channel.send("An Error Occurred While Try To Play!", silent=True), self.bot.loop)
            return

        if self.queue.loop_mode == "2":
            self.queue.appendleft_current(self.current_query) 
        elif self.queue.loop_mode == "3":
            self.queue.append_current(self.current_query)
        
        self.bot.loop.call_soon_threadsafe(self.next_song_event.set)

        if self.queue.is_empty:
            if self.text_channel:
                asyncio.run_coroutine_threadsafe(self.voice.channel.edit(status=f'Noob Bot: Nothing In Is Playing Now!', reason=f"Update The Playing Music For {str(self.voice.channel.name)}"), self.bot.loop)
                asyncio.run_coroutine_threadsafe(self.text_channel.send("Queue Is Right Now Empty!"), self.bot.loop)

    def pause(self):
        if self.voice and self.voice.is_playing():
            self.voice.pause()

    def resume(self):
        if self.voice and self.voice.is_paused():
            self.voice.resume()

    def skip(self):
        if self.voice and self.voice.is_playing():
            self.voice.stop()
