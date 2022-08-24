import os
import nextcord
import asyncio
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
import pymongo
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, CursorNotFound
import aiohttp
from utils.manga_helper import *

GUILD_IDS = [847268531648462860, 930961690672128000, 998379655906213918]


class Manga(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name='manga', description='Searches for a manga', guild_ids=GUILD_IDS)
    async def manga(self, interaction: Interaction, query: str = SlashOption(name="name", required=True)):
        await interaction.response.defer()
        embed = await search_manga(query, 1)
        await interaction.followup.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Manga(bot))
