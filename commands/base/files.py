import discord
import os
import tempfile

import botconfig as config
from discord import app_commands
from discord.ext import commands

from library.core.helpmodule import textfilter
from library.core import console
from library.core.cmdhelpermodule import googttshelper as tts
from library.core.cmdhelpermodule import gifcreator
from library.core.helpmodule.randomtextcreator import GetRandomText
from library.core.helpmodule import temphost as tmphost

def setup(bot):

    @bot.tree.command(
        name="tts",
        description="Convert Your Text To TTS Audio! (Filter Needed)"
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
    @app_commands.describe(text="The Text You Want To Convert To TTS Audio")
    async def tts_command(interaction: discord.Interaction, text: str):
        await interaction.response.defer()

        filtered_text = textfilter.FilterStringAsync(text)

        audio_path, detected_lang = tts.TTSNow(filtered_text)
        if not os.path.isfile(audio_path):
            await interaction.followup.send(f"Hey {interaction.user.mention}!\nI Think Something Went Wrong While Generating TTS Audio!")
            return
        
        file_size = os.path.getsize(audio_path)
        if file_size >= 8 * 1024 * 1024:
            await interaction.followup.send(f"Hey {interaction.user.mention}!\nI Think The Generated TTS Audio Is Too Large To Send (Max 8MB)")
            os.remove(audio_path)
            return
        
        discord_file = discord.File(audio_path, filename=f"{interaction.user.id}-{detected_lang.upper()}.mp3")
        await interaction.followup.send(content=f"TTS Request From **{interaction.user.mention}** Was Done!\n-# Using Language: **{detected_lang.upper()}**\n-# TTS From: {filtered_text}", file=discord_file)

        os.remove(audio_path)
    
    
    @bot.tree.command(
        name="creategif",
        description="Turn Your MP4 Video Into A Gif!"
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
    @app_commands.describe(video="The MP4 Video You Want To Convert To GIF (Big File May Result In Lower FPS)")
    async def gif(interaction: discord.Interaction, video: discord.Attachment):
        await interaction.response.defer()

        if not video.content_type or not video.content_type.startswith("video/"):
            await interaction.followup.send(f"Hey {interaction.user.mention}!\nThe Provided Attachment Is Not A Video!")
            return

        if video.size >= 8 * 1024 * 1024:
            await interaction.followup.send(f"Hey {interaction.user.mention}!\nThe Provided Video Is Too Large To Process! (Max 8MB)")
            return
        try:
            result_file = await gifcreator.ConvertToGif(video.url)

            if not os.path.isfile(result_file):
                await interaction.followup.send(f"Hey {interaction.user.mention}!\nGIF File Was Not Created Due The Error Or Something!")
                raise RuntimeError("GIF File Was Not Created Due The Error Or Something!")

            if os.path.getsize(result_file) >= 8 * 1024 * 1024:
                os.remove(result_file)
                await interaction.followup.send(f"Hey {interaction.user.mention}!\nThe Generated GIF Is Was Too Big To Send! (Max 8MB)")
                return

            discord_file = discord.File(result_file, filename=f"{GetRandomText()}.gif")

            await interaction.followup.send(content=f"GIF Conversion Request From {interaction.user.mention} Was Done!", file=discord_file)

            os.remove(result_file)
        except Exception as e:
            await interaction.followup.send(f"Hey {interaction.user.mention}!\nSomething Went Wrong While Converting Your Video Into A GIF")
            console.warn(f"Error While Making GIF As: {e}")

    
    @bot.tree.command(
        name="templink",
        description="Convert Your File Into A Temporary Direct CDN Link! (7 Days Long)"
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
    @app_commands.describe(file="The File That You Want to Convert To Temporary Link!")
    async def getlink(interaction: discord.Interaction, file: discord.Attachment):
        await interaction.response.defer()

        temp_folder = os.path.join(
            tempfile.gettempdir(),
            config.BotOwnerTeam,
            config.AppName,
            "temporary",
            "filetolink"
        )
        os.makedirs(
            temp_folder,
            exist_ok=True
        )

        if not file.content_type:
            await interaction.followup.send(f"Hey {interaction.user.mention}!\nI Cannot Check Your File!")
            return

        try:
            file_extension = file.filename.split(".")[-1]
            temp_filename = f"tmp_{GetRandomText()}.{file_extension}"
            temp_path = os.path.join(
                temp_folder,
                temp_filename
            )
            
            await file.save(temp_path)

            link = tmphost.ConvertFileIntoLink(
                temp_path,
                True
            )
            if link:
                await interaction.followup.send(f"Hey {interaction.user.mention}!\nYour Temp Link Are Done!\n\nHere It's It: {link}\n\n**To Know What You Can Use Link For Please Run `/documentations doc:templink`**\n\n-# Please Note: The Link Will Expired In 7 Days!")
            else:
                await interaction.followup.send(f"Hey {interaction.user.mention}!\nI Think There Are Error While Making Temp Link!")

        except Exception as e:
            console.warn(f"Hey {interaction.user.mention}!\nI Got Error While Making Temp Link As: {e}")
            await interaction.followup.send(f"There Are Some Error Happend On Our Server!")