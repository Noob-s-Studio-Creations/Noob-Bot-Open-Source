import discord
import asyncio

from discord import app_commands
from deep_translator import GoogleTranslator

from library.core.helpmodule import textfilter

def setup(bot):
    @bot.tree.context_menu(name="Translate This")
    @app_commands.allowed_installs(
        guilds=True,
        users=True
    )
    @app_commands.allowed_contexts(
        guilds=True,
        dms=True,
        private_channels=True
    )
    async def translate_message(interaction: discord.Interaction, message: discord.Message):
        await interaction.response.defer(thinking=True, ephemeral=True)

        filtered_message = await asyncio.to_thread(
            textfilter.FilterStringAsync,
            message.content
        )

        target_lang = interaction.locale.value.split("-")[0]

        is_susess = False

        try:
            translated = GoogleTranslator(
                source="auto",
                target=target_lang
            ).translate(filtered_message)
            is_susess = True
        except Exception:
            translated = filtered_message
            is_susess = False

        if is_susess == False:
            await interaction.followup.send(
                f"Sorry But... Translate Failed :P",
                ephemeral=True
            )
        else:
            await interaction.followup.send(
                f"**Translated Message\n-# Note: Translation Are Based From Your Discord Languge ({str(target_lang).upper()})**\n```\n{translated}\n```",
                ephemeral=True
            )