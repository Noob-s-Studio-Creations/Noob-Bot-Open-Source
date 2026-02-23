import discord
import asyncio

from discord import app_commands
from discord.ext import commands

from library.roblox import games
from library.core.helpmodule.numberstringconverto import ConverToNumberThatAbleToRead

def setup(bot):

    @bot.tree.command(
        name="rbxgame",
        description="Get Roblox Game Info By PlaceId Or UniverseId"
    )
    @app_commands.describe(id="The PlaceId Or UniverseId Of The Roblox Game")
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
    async def rbxgame(interaction: discord.Interaction, id: int):
        await interaction.response.defer()

        game_info = await asyncio.to_thread(
            games.GetGameInfoAsync,
            id
        )

        if "error" in game_info:
            await interaction.followup.send(f"Hey {interaction.user.mention}!\nI Think Something Went Wrong While Freshing Your Given Game Info!")
            return

        embed = discord.Embed(
            url=f"https://roblox.com/games/{game_info.get('rootPlaceId', '1818')}",
            title=game_info.get(
                "name",
                "Unknown Game"
            ),
            color=discord.Color.gold()
        )

        embed.add_field(
            name="UniverseId",
            value=game_info.get('universeId', '0'),
            inline=True
        )
        embed.add_field(
            name="RootPlaceId",
            value=game_info.get('rootPlaceId', '0'),
            inline=True
        )

        resault_creatorstring = f"{game_info.get('creator', {}).get('name', 'Unknown')} ({game_info.get('creator', {}).get('type', 'N/A0')})"
        if game_info.get('creator', {}).get('type', 'N/A').lower() == "user":
            resault_creatorstring = f"[{game_info.get('creator', {}).get('name', 'Unknown')} ({game_info.get('creator', {}).get('type', 'N/A')})](https://www.roblox.com/users/{str(game_info.get('creator', {}).get('id', '9778511204'))}/profile)"
        elif game_info.get('creator', {}).get('type', 'N/A').lower() == "group":
            resault_creatorstring = f"[{game_info.get('creator', {}).get('name', 'Unknown')} ({game_info.get('creator', {}).get('type', 'N/A')})](https://www.roblox.com/communities/{str(game_info.get('creator', {}).get('id', '713383747'))})"
        else:
            resault_creatorstring = f"{game_info.get('creator', {}).get('name', 'Unknown')} ({game_info.get('creator', {}).get('type', 'N/A')})"
            
        embed.add_field(
            name="Creator",
            value=resault_creatorstring,
            inline=True
        )

        embed.add_field(
            name="Visits",
            value=str(ConverToNumberThatAbleToRead(int(game_info.get('visits', '0')))),
            inline=True
        )
        embed.add_field(
            name="Favorites",
            value=str(ConverToNumberThatAbleToRead(int(game_info.get('favorites', '0')))),
            inline=True
        )
        embed.add_field(
            name="Max Players",
            value=game_info.get('maxPlayers', "0"),
            inline=True
        )
        embed.add_field(
            name="Now Playing",
            value=str(ConverToNumberThatAbleToRead(int(game_info.get('playing', '0')))),
            inline=True
        )
        embed.add_field(
            name="Up Votes",
            value=ConverToNumberThatAbleToRead(int(game_info.get('votes', {}).get('up', '0'))),
            inline=True
        )
        embed.add_field(
            name="Down Votes",
            value=ConverToNumberThatAbleToRead(int(game_info.get('votes', {}).get('down', '0'))),
            inline=True
        )
        embed.add_field(
            name="Votes",
            value=f"{ConverToNumberThatAbleToRead(int(game_info.get('votes', {}).get('percent', '0')))}%",
            inline=True
        )

        embed.add_field(
            name="Description",
            value=game_info.get('description', 'No Description') or 'No Description',
            inline=False
        )

        embed.set_image(
            url=game_info.get(
                "thumbnail",
                "https://prayoadmii.neocities.org/Assets/CDN/dsbot-rblx-place-thumb-placeholder.png"
            ) or "https://prayoadmii.neocities.org/Assets/CDN/dsbot-rblx-place-thumb-placeholder.png"
        )
        embed.set_thumbnail(
            url=game_info.get(
                "icon",
                "https://prayoadmii.neocities.org/Assets/CDN/dsbot-rblx-place-placeholder.png"
            ) or "https://prayoadmii.neocities.org/Assets/CDN/dsbot-rblx-place-placeholder.png"
        )

        await interaction.followup.send(embed=embed)