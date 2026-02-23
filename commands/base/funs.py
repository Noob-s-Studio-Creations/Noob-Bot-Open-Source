import discord
import datetime

from discord import app_commands
from discord.app_commands import Choice

def setup(bot):

    @bot.tree.command(
        name="prayoadmiitime",
        description="Get Current Time For PrayoadMii"
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
    @app_commands.describe(hrs12="Do You Want 12 Hours Time Format? (Default Is No)")
    @app_commands.choices(
        hrs12=[
            Choice(name="Yes", value="Yes"),
            Choice(name="No", value="No")
        ]
    )
    async def prayoadmiitime(interaction: discord.Interaction, hrs12: str = "No"):
        await interaction.response.defer()

        now = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=7)))

        GMT7_24HRS = f"{now:%H:%M}"
        GMT7_12HRS = f"{now:%I:%M %p}"

        Res =  GMT7_12HRS if hrs12 == "Yes" else GMT7_24HRS
        
        await interaction.followup.send(f"Current Time For PrayoadMii Is: {Res}")
    

    @bot.tree.command(
        name="install",
        description="Install The Bot To Your Server Or Your Self!"
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
    async def install(interaction: discord.Interaction):
        await interaction.response.defer()

        await interaction.followup.send(f"## Hey! {interaction.user.mention}!\nLook Like You're Ready To Install Me On Your Server!\n\n**[New]: User Install - Install Me And Use My Commands Everyware On Discord!**\n\nSo You Can Install Me With This [Install Link](https://discord.com/oauth2/authorize?client_id=1354829549577437214)\n\n**User Install:** Click Install Link Then Choose **User Install** Then Complete The Installation Process!\n\n**Server Install:** Click Install Link Then Choose **Add To Servers** Then Select Your Target Server And Complete The Installation Process!")

    
    @bot.tree.command(
        name="nothing",
        description="I Told You! This Is Nothing!"
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
    async def nothing(interaction: discord.Interaction):
        await interaction.response.defer()

        await interaction.followup.send("⠀ ⠀")