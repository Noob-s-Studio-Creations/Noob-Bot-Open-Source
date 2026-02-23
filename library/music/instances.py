from library.music.player import MusicPlayer
from library.core import console

players = {}

def get_player(guild, bot):
    if guild.id not in players:
        players[guild.id] = MusicPlayer(guild, bot)
        console.info(f"Created Voice Instances ID: {str(guild.id)} | Total Instances: {str(len(players))}")
    
    return players[guild.id]