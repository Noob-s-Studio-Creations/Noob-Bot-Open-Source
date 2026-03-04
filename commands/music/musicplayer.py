import discord

from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice

from library.music.instances import get_player
from library.music.embedui import QueueView

def setup(bot: commands.bot.Bot):
    @bot.tree.command(
        name="add",
        description="Play Music Or Add That To Queue"
    )
    @app_commands.allowed_contexts(
        guilds=True,
        dms=False,
        private_channels=True
    )
    async def play(interaction: discord.Interaction, query: str):
        await interaction.response.defer()

        if not interaction.user.voice:
            await interaction.followup.send(f"Hey {interaction.user.mention}... Can You Plz Join Any Of Voice Channel?")
            return

        player = get_player(interaction.guild, bot)
        player.text_channel = interaction.channel

        await player.connect(interaction.user.voice.channel)
        title = await player.add_song(query)
        if not title:
            await interaction.followup.send(f"Hey {interaction.user.mention}!\nSomething Was Wrong While Adding The Song!")
            return

        await interaction.followup.send(f"I'm Added: **{title}**")

    @bot.tree.command(
        name="skip",
        description="Skip Current Song (Can Use For Stop Too!)"
    )
    @app_commands.allowed_contexts(
        guilds=True,
        dms=False,
        private_channels=True
    )
    async def skip(interaction: discord.Interaction):
        await interaction.response.defer()

        player = get_player(interaction.guild, bot)
        player.skip()

        await interaction.followup.send("## MUSIC SKIPPED!")

    @bot.tree.command(
        name="loop",
        description="Set How The Bot Will Loop Your Music"
    )
    @app_commands.allowed_contexts(
        guilds=True,
        dms=False,
        private_channels=True
    )
    @app_commands.describe(mode="Select How I Will Loop Music For You?")
    @app_commands.choices(
        mode=[
            Choice(name="Playlist", value="3"),
            Choice(name="Ones", value="2"),
            Choice(name="Off", value="1")
        ]
    )
    async def loop(interaction: discord.Interaction, mode: str):
        await interaction.response.defer()

        player = get_player(interaction.guild, bot)

        mode = mode.lower()
        if mode not in ("1", "2", "3"):
            await interaction.followup.send(f"{interaction.user.mention}... Can You Plz Use: `Off`, `Ones`, Or `Playlist`?")
            return

        player.queue.loop_mode = mode

        ModeName = "Off"
        if mode == "1":
            ModeName = "Off"
        elif mode == "2":
            ModeName = "Ones"
        else:
            ModeName = "Playlist"

        await interaction.followup.send(f"The Song Will Now Loop As: **{ModeName}**")

    @bot.tree.command(
        name="queue",
        description="Show Music Queue"
    )
    @app_commands.allowed_contexts(
        guilds=True,
        dms=False,
        private_channels=True
    )
    async def queue_cmd(interaction: discord.Interaction):
        await interaction.response.defer()

        player = get_player(interaction.guild, bot)

        if player.queue.is_empty:
            await interaction.followup.send(f"{interaction.user.mention}\nThe Queue Is Look So Empty!\n-# Add Something Now?")
            return

        embed = discord.Embed(
            title="MUSIC QUEUE",
            color=discord.Color.blue()
        )

        for i, song in enumerate(list(player.queue.queue)[:10], start=1):
            embed.add_field(name=f"{i}. {song}", value="\u200b", inline=False)

        await interaction.followup.send(embed=embed, view=QueueView(player))
