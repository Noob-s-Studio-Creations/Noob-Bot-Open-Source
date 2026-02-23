import discord
import asyncio

from discord import app_commands
from discord.ext import commands

from library.roblox import groups

def setup(bot):

    @bot.tree.command(
        name="rbxgroup",
        description="Get Roblox Group Info By GroupId"
    )
    @app_commands.describe(id="The GroupId Of The Roblox Group")
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
    async def rbxgroup(interaction: discord.Interaction, id: int):
        await interaction.response.defer()

        group_info = await asyncio.to_thread(
            groups.GetRoGroupInfo,
            id
        )

        if not group_info:
            await interaction.followup.send(f"{interaction.user.mention} I Got Error While Freshing Group Info!")
        
        embed = discord.Embed(
            url=f"https://roblox.com/communities/{group_info.get('id')}",
            title=group_info.get('name'),
            color=discord.Color.blue()
        )

        embed.add_field(
            name="Group Id",
            value=group_info.get('id'),
            inline=True
        )
        embed.add_field(
            name="Owner",
            value=f"[{group_info.get('owner', {}).get('name', 'Unknown')}](https://roblox.com/users/{group_info.get('owner', {}).get('id', '9778511204')}/profile)",
            inline=True
        )

        has_Vbadge = "Yup! They Did!" if group_info['hasVBadge'] else "Nope"
        embed.add_field(
            name="Got Verified Badge?",
            value=has_Vbadge,
            inline=True
        )

        embed.add_field(
            name="Description",
            value=group_info.get('description', 'No Description') or 'No Description',
            inline=False
        )

        embed.set_thumbnail(url=group_info.get('icon'))

        await interaction.followup.send(embed=embed)