import discord

from discord import app_commands
from discord.app_commands import Choice

from library.music.instances import get_player
from library.music.embedui import QueueView

def setup(bot):
    @bot.tree.command(
        name="pause",
        description="Pause The Music"
    )
    @app_commands.allowed_contexts(
        guilds=True,
        dms=False,
        private_channels=True
    )
    async def pause(interaction: discord.Interaction):
        await interaction.response.defer()

        player = get_player(interaction.guild, bot)
        player.pause()

        await interaction.followup.send("## MUSIC PAUSED!")

    @bot.tree.command(
        name="resume",
        description="Resume The Music"
    )
    @app_commands.allowed_contexts(
        guilds=True,
        dms=False,
        private_channels=True
    )
    async def resume(interaction: discord.Interaction):
        await interaction.response.defer()

        player = get_player(interaction.guild, bot)
        player.resume()

        await interaction.followup.send("## MUSIC RESUMED!")