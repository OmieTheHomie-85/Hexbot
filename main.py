import os
import nextcord
import aiosqlite
import asyncio
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption, ChannelType
from os import getenv
from itertools import cycle
from dotenv import load_dotenv
from nextcord.abc import GuildChannel
import pymongo
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, CursorNotFound


PREFIX = "&"
GUILD_IDS = [847268531648462860]

bot = commands.Bot(command_prefix=commands.when_mentioned_or(PREFIX), owner_id=441184331826987019,
                   enable_debug_events=True)
status = cycle(["&help", "Help me I am dying!", "IT’S ABOUT DRIVE 🥶 IT’S ABOUT POWER 💪 WE STAY HUNRGY 💯 WE DEVOUR "
                                                "🥱 PUT IN THE WORK 🥵 PUT IN THE HOURS 😎 AND TAKE WHAT’S OURS 💰"])
load_dotenv()

colors = [0xffffff, 0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0x00FFFF, 0xFF00FF]
nl = '\n'


# Cogs
@bot.command()
@commands.is_owner()
async def reload(ctx, extension=None):
    if extension is None:
        for file_name in os.listdir('./cogs'):
            if file_name.endswith(".py"):
                bot.unload_extension(f'cogs.{file_name[:-3]}')
                bot.load_extension(f'cogs.{file_name[:-3]}')
    else:
        bot.unload_extension(f'cogs.{extension}')
        bot.load_extension(f'cogs.{extension}')


@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')


@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')


@bot.event
async def on_ready():
    print('bot is ready')
    await custom_status.start()




for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')





# Error handling
@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"{error}")


@tasks.loop(seconds=30)
async def custom_status():
    await bot.change_presence(activity=nextcord.Game(next(status)))


@bot.event
async def on_ready():
    await custom_status.start()
    print("THE BOT IS ON")


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.unload_extension(f'cogs.{filename[:-3]}')
        bot.load_extension(f'cogs.{filename[:-3]}')


# basic commands
@bot.slash_command(guild_ids=GUILD_IDS)
async def ping(interaction: Interaction):
    ping_embed = nextcord.Embed(title="Pong!")
    ping_embed.add_field(name='your ping to bot: ', value=f'{round(bot.latency * 1000)}')
    await interaction.send(embed=ping_embed)







bot.run(getenv('TOKEN'))
