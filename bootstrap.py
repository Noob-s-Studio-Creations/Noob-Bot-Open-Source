import discord
import os
import importlib
import logging

from discord.ext import commands
import botconfig as config

from library.core import console
from library.music.instances import get_player
from library.core import servertype

D_Intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix=config.CommandPrefix,
    intents=D_Intents
)

D_Player_Logger = logging.getLogger("discord.player")
D_Player_Logger.setLevel(logging.WARNING)

channel = config.ServerName
if servertype.get_platform() == "win":
    os.system("cls")
    channel = config.DEVServerName
else:
    os.system("clear")
    channel = config.ServerName

def load_commands(bot):
    commands_dir = os.path.join(os.path.dirname(__file__), "commands")

    for root, dirs, files in os.walk(commands_dir):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                rel_dir = os.path.relpath(root, os.path.dirname(__file__))

                module_path = (
                    rel_dir.replace(os.sep, ".") + "." + file[:-3]
                )

                try:
                    module = importlib.import_module(module_path)
                    
                    if hasattr(module, "setup"):
                        module.setup(bot)
                except Exception as e:
                    console.warn(f"Something Was Wrong While Loading Commands From {str(module_path)} As: {str(e)}")
    console.info("All Commands Modules Was Loaded Successfully!")

load_commands(bot)

@bot.command(
    name="sync",
    help="Sync Slash Commands For Your Server! (Admin Only)"
)
@commands.has_permissions(administrator=True)
async def sync(ctx):
    try:
        await bot.tree.sync(guild=ctx.guild)
        await ctx.send("Synced Slash Commands To This Server!")

        console.log(f"Synced Slash Commands To Server: {ctx.guild.name} ({ctx.guild.id})")
    except Exception as e:
        await ctx.send("Error While Syncing Commands")
        console.error(f"Error While Sync Commands As: {e}")

@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is not None:
        voice_channel = before.channel
        player = get_player(voice_channel.guild, bot)

        if player and player.voice and player.voice.channel == voice_channel:
            non_bot_members = [
                m for m in voice_channel.members if not m.bot or m.id == bot.user.id
            ]

            if len(non_bot_members) == 1 and non_bot_members[0].id == bot.user.id:
                console.log("Leaving Bot Due No Members In Voice Channel Or Bot Got Kicked!")
                try:
                    await player.disconnect()
                except Exception as e:
                    console.warn(f"Something Went Wrong While Disconnecting As: {e}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Bro What? 🤨 I Think I Don't Know Command Named `{ctx.message.content}`!")
        return
    elif isinstance(error, commands.errors.MissingPermissions):
        await ctx.send(f"Hey! You're Missing Some Permissions To Use That Command!")
        return
    raise error

@bot.event
async def on_ready():
    console.log(f"Bot Installed In: {len(bot.guilds)} Server{'s' if len(bot.guilds) != 1 else ''}")
    console.log(f"Server Channel: {channel}")

    PLATFORM = servertype.get_platform()

    if PLATFORM == "rpi":
        console.info("Server Is Started As Raspberry Pi")
    elif PLATFORM == "linx":
        console.info("Server Is Started As Linux Server")
    elif PLATFORM == "win":
        console.info("Server Is Started As Windows Server")
    else:
        console.warn("Incompleteable Server... Something May Not Work!")

    console.log(f"App Version: {config.VersionId}")
    console.info(f"Bot Is Right Now Online As: {bot.user.name} ({bot.user}) (Bot User Id: {bot.user.id})")

    await bot.change_presence(
        activity=discord.CustomActivity(
            name=f"Running On An {channel} Server!"
        ),
        status=discord.Status.online
    )
    try:
        synced = await bot.tree.sync()

        console.info(f"We're Now Sync All {len(synced)} Commands Successfully!")
    except Exception as e:
        console.warn(f"Some Exception While Syncing Commands As: {e}")
        console.warn("New Command Will Not Added Until Next StartUp Or Manual Sync!")

bot.run(
    str(config.Discord_Bot_Token),
    reconnect=True
)