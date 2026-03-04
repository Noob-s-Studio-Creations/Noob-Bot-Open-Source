import discord
import tempfile
import os

import botconfig as config

from discord.ext import commands
from discord import app_commands

def CheckBotTempUsageAsMB():
    bot_temp_dir = os.path.join(
        tempfile.gettempdir(),
        config.BotOwnerTeam,
        config.AppName
    )

    if not os.path.exists(bot_temp_dir):
        return 0.0

    total_size = 0

    for dirpath, _, filenames in os.walk(bot_temp_dir):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                total_size += os.path.getsize(fp)
            except OSError:
                pass
    
    return total_size / (1024 * 1024)

def setup(bot: commands.bot.Bot):

    @bot.tree.command(
        name="botstat",
        description="Get Current Bot Statistics"
    )
    @app_commands.allowed_installs(
        guilds=True,
        users=True
    )
    @app_commands.allowed_contexts(
        guilds=True,
        dms=True,
        private_channels=True
    )
    async def botstat(interaction: discord.Interaction):
        await interaction.response.defer()

        embed = discord.Embed(
            title="Bot Status",
            color=discord.Color.gold()
        )
        embed.add_field(
            name="Ping",
            value=f"{round(bot.latency * 1000)} ms",
            inline=True
        )
        embed.add_field(
            name="Version",
            value=config.VersionId,
            inline=True
        )
        embed.add_field(
            name="Installed In",
            value=f"{str(len(bot.guilds))} Server{'s' if len(bot.guilds) != 1 else ''}",
            inline=False
        )
        embed.add_field(
            name="Connected VC",
            value=f"{str(len(bot.voice_clients))}",
            inline=True
        )

        await interaction.followup.send(embed=embed)