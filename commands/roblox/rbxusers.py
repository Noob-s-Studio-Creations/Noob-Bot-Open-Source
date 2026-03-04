import discord
import asyncio

from discord import app_commands
from discord.ext import commands

from library.roblox import users as rbxuser

def setup(bot: commands.bot.Bot):
    @bot.tree.command(
        name="rbxuser",
        description="Find A Roblox User By Their Username"
    )
    @app_commands.describe(username="The Username Of The Roblox User (User ID Don't Count!)")
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
    async def robloxfind(interaction: discord.Interaction, username: str):
        await interaction.response.defer()

        user_data, error_id = await asyncio.to_thread(
            rbxuser.GetUserByUsernameAsync,
            username
        )

        if user_data is None:
            if error_id == 429:
                await interaction.followup.send(f"{interaction.user.mention}... I Think Rate Limit Was Reached... So Can You Able To Try Again Later?")
                return

            await interaction.followup.send(f"Hey {interaction.user.mention}!\nThis Player Din't Exist Or Something Went Wrong With The Roblox Server!")
            return

        embed = discord.Embed(
            url=f"https://roblox.com/users/{user_data['id']}/profile",
            title=f"Roblox User Info: {user_data['name']}",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(
            url=user_data['profile_picture'] or "https://prayoadmii.neocities.org/Assets/CDN/dsbot-rblx-avatar-placeholder.png"
        )
        embed.add_field(
            name="User ID",
            value=user_data['id'],
            inline=True
        )
        embed.add_field(
            name="Display Name",
            value=user_data['display_name'],
            inline=True
        )

        is_banned = "Yup!" if user_data['banned'] else "Nope"
        embed.add_field(
            name="Was Banned?",
            value=is_banned,
            inline=True
        )

        has_badge = "Yup! They Did!" if user_data['hasVerifiedBadge'] else "Nope"
        embed.add_field(
            name="Got Verified Badge?",
            value=has_badge,
            inline=True
        )

        embed.add_field(
            name="Description",
            value=user_data['description'] or "No Description",
            inline=False
        )

        await interaction.followup.send(embed=embed)
