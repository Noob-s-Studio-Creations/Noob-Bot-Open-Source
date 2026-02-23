import discord

from discord import app_commands

from library.music.instances import get_player

def setup(bot):
    @bot.tree.command(
        name="join",
        description="Make Me Join Your Voice Channel!"
    )
    @app_commands.allowed_contexts(
        guilds=True,
        dms=False,
        private_channels=True
    )
    async def join(interaction: discord.Interaction):
        await interaction.response.defer()

        if not interaction.user.voice:
            await interaction.followup.send(f"Hey {interaction.user.mention}... Can You Plz Join Any Of Voice Channel?")
            return

        player = get_player(interaction.guild, bot)
        await player.connect(interaction.user.voice.channel)

        await interaction.followup.send(f"I'm Joined **{interaction.user.voice.channel.name}**")

    @bot.tree.command(
        name="leave",
        description="Make Me Gone!"
    )
    @app_commands.allowed_contexts(
        guilds=True,
        dms=False,
        private_channels=True
    )
    async def leave(interaction: discord.Interaction):
        await interaction.response.defer()

        player = get_player(interaction.guild, bot)
        await player.disconnect()

        await interaction.followup.send("# I'M GONE!")