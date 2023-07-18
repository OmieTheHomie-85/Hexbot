import math
import re

import nextcord
from nextcord import Embed
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
import wavelink
from wavelink.queue import QueueEmpty
from wavelink.ext import spotify
import datetime
from utils.music_helper import *


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self.node_connect())

    async def node_connect(self):
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(bot=self.bot,
                                            host='jonnythedev.com',
                                            port=2333,
                                            password='QEpvbm55MDUxMA==')

    @nextcord.slash_command(description="Play a song in a voice chat")
    async def play(self, interaction:Interaction, search: str = SlashOption(description="Search for a song")):
        search = await wavelink.YouTubeTrack.search(query=search, return_first=True)
        if not interaction.guild.voice_client:
            vc: wavelink.Player = await interaction.user.voice.channel.connect(cls=wavelink.Player)
        elif not getattr(interaction.user.voice, "channel", None):
            return await interaction.send("Join a voice channel and run this command again")
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        if vc.is_playing:
            vc.queue.put(search)
            await vc.play(search)
        else:
            await vc.play(search)


def setup(bot: commands.Bot):
    bot.add_cog(Music(bot))
