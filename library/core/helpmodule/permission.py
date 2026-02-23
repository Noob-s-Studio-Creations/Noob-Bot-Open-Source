import discord

from typing import Iterable, Optional, Union

from library.core import console

def CheckNeedPermission(targetchannel: discord.abc.GuildChannel, neededpermission: Union[Iterable[str], discord.Permissions], interaction: Optional[discord.Interaction] = None, bot: Optional[Union[discord.Client, discord.ext.commands.Bot]] = None) -> bool:
    if interaction is None and bot is None:
        console.warn("Please Provide Bot Or Interaction!")
        return False

    if interaction:
        guild = interaction.guild
        me = guild.me
    else:
        guild = targetchannel.guild
        me = guild.me

    if not guild or not me:
        console.warn("Guild Or Bot Member Was Not Found!")
        return False

    perms = targetchannel.permissions_for(me)

    if isinstance(neededpermission, (list, tuple)):
        for perm in neededpermission:
            if not getattr(perms, perm, False):
                return False
        return True

    if isinstance(neededpermission, discord.Permissions):
        return perms >= neededpermission

    console.warn("Invalid neededpermission Table Format!")
    return False
