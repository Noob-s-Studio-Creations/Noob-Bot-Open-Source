import discord
import asyncio
import os

from discord.app_commands import Choice
from discord.ext import commands
from discord import app_commands

from library.core.helpmodule.randomtextcreator import GetRandomText
from library.core.helpmodule import textfilter
from library.core.cmdhelpermodule import memeimagecreator as memeedit
from library.core import console

def setup(bot):
    
    @bot.tree.command(
        name="memecaption",
        description="Add Caption Text To Your Image! (Filter Needed!)"
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
    @commands.has_permissions(attach_files=True)
    @app_commands.describe(image="The Image You Want To Edit!", caption="The Caption Text You Want To Add!")
    async def edit(interaction: discord.Interaction, image: discord.Attachment, caption: str):
        await interaction.response.defer()

        output_path = None

        filtered_message = await asyncio.to_thread(
            textfilter.FilterStringAsync,
            caption
        )

        if not image.content_type or not image.content_type.startswith("image/"):
            await interaction.followup.send(f"{interaction.user.mention} Can U Plz Upload An Image???")
            return

        try:
            output_path = await memeedit.AddMemeCaption(
                image,
                filtered_message
            )

            await interaction.followup.send(
                content=f"Caption Request From {interaction.user.mention} Was Done!",
                file=discord.File(output_path, filename=f"{GetRandomText()}.jpg")
            )
        except Exception as e:
            await interaction.followup.send(
                f"{interaction.user.mention} I Got Error While Creating Caption For You!!!"
            )

            console.warn(f"Error While Creating Meme Caption As: {e}")
        finally:
            if output_path and os.path.exists(output_path):
                os.remove(output_path)