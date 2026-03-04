import discord
import os

from discord import app_commands
from discord.ext import commands

from library.core.helpmodule.randomtextcreator import GetRandomText

MAX_MESSAGE_LENGTH = 1900

def setup(bot: commands.bot.Bot):

    @bot.tree.command(
        name="documentations",
        description="Find Documentations On The Command Or Features You Need!"
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
    @app_commands.describe(
        doc="Documentation Name Or Command Name You Want to Know About!"
    )
    async def senddocs(interaction: discord.Interaction, doc: str):
        await interaction.response.defer(ephemeral=True)

        CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
        PROJECT_ROOT = os.path.abspath(
            os.path.join(
                CURRENT_DIR,
                "..",
                ".."
            )
        )

        docs_dir = os.path.join(
            PROJECT_ROOT,
            "assets",
            "documents"
        )

        safe_name = os.path.basename(doc)
        docs_book_path = os.path.join(docs_dir, f"{safe_name.lower().replace(' ', '')}.txt")

        if not os.path.isfile(docs_book_path):
            await interaction.followup.send(
                "Documentation For That Command Or Feature Was Not Found!",
                ephemeral=True
            )
            return

        with open(docs_book_path, "r", encoding="utf-8") as f:
            content = f.read()

        if len(content) <= MAX_MESSAGE_LENGTH:
            await interaction.followup.send(
                f"Ok {interaction.user.mention} Here Is The Docs You're Finding For!\n\n>>> {content}",
                ephemeral=True
            )
        else:
            file = discord.File(
                docs_book_path,
                filename=f"{GetRandomText(5)}.txt"
            )

            await interaction.followup.send(
                content="Documentation Was Too Long... So I Will Send To You As File!",
                file=file,
                ephemeral=True
            )
