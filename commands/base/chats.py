import discord
import asyncio

from library.core.helpmodule import textfilter

from discord import app_commands
from discord.ext import commands

def setup(bot: commands.bot.Bot):
    @bot.tree.command(
        name="prayoadmiistyle",
        description="Turn Your Messages Into PrayoadMii Style (Filtered Needed!)"
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
    async def prayoadmiistyle(interaction: discord.Interaction, message: str):
        await interaction.response.defer()

        filtered_message = await asyncio.to_thread(
            textfilter.FilterStringAsync,
            message
        )
        transformed_message = ' '.join(word.capitalize() for word in filtered_message.split())

        cleaned = filtered_message.replace(" ", "").lower()

        if "@everyone" in cleaned:
            await interaction.followup.send(f"AYO {interaction.user.mention}!\nI NOT GONNA PING EVERYONE!!!")
            return
        elif "@here" in cleaned:
            await interaction.followup.send(f"AYO {interaction.user.mention}!\nI NOT GONNA PING HERE!!!")
            return

        await interaction.followup.send(str(transformed_message).replace("\\n", "\n"))


    @bot.tree.command(
        name="filter",
        description="Filter The Bad Words Out From Your Message Text"
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
    async def filter_cmd(interaction: discord.Interaction, message: str):
        await interaction.response.defer(ephemeral=True)

        filtered_message = await asyncio.to_thread(
            textfilter.FilterStringAsync,
            message
        )
        
        cleaned = filtered_message.replace(" ", "").lower()

        if "@everyone" in cleaned:
            await interaction.followup.send("AYO!!! I NOT GONNA PING EVERYONE!!!", ephemeral=True)
            return
        elif "@here" in cleaned:
            await interaction.followup.send("AYO!!! I NOT GONNA PING HERE!!!", ephemeral=True)
            return

        await interaction.followup.send(str(filtered_message).replace("\\n", "\n"), ephemeral=True)


    @bot.tree.command(
        name="echo",
        description="Make Bot Say Anything You Want! (Filtered First)"
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
    async def say(interaction: discord.Interaction, message: str):
        await interaction.response.defer()

        filtered_message = await asyncio.to_thread(
            textfilter.FilterStringAsync,
            message
        )

        cleaned = filtered_message.replace(" ", "").lower()

        if "@everyone" in cleaned:
            await interaction.followup.send(f"AYO {interaction.user.mention}!\nI NOT GONNA PING EVERYONE!!!")
            return
        elif "@here" in cleaned:
            await interaction.followup.send(f"AYO {interaction.user.mention}!\nI NOT GONNA PING HERE!!!")
            return

        await interaction.followup.send(str(filtered_message).replace("\\n", "\n"))