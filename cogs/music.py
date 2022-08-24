import math
import re
from nextcord import Embed
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
import wavelink
from wavelink.queue import QueueEmpty
from wavelink.ext import spotify
import datetime
from utils.music_helper import *

GUILD_IDS = [847268531648462860, 998379655906213918]


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self.node_connect())

    async def node_connect(self):
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(bot=self.bot, host='lavalinkinc.ml', port=443, password='incognito',
                                            https=True, spotify_client=spotify.SpotifyClient(client_id="72b562bb80bf4e44a2ffdbbdee9a105e", client_secret="e5c08ebdfad04167b42ae7a1789c7273"))

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f'Node:<{node.identifier}> is ready!!')

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track: wavelink.YouTubeTrack, reason):
        interaction = player.interaction
        vc: player = interaction.guild.voice_client

        if vc.loop:
            return await vc.play(track)
        next_song = vc.queue.get()
        await vc.play(next_song)
        await interaction.send(f"Now Playing: {next_song.title}")

    @nextcord.slash_command(description="Play a song in a voice chat", guild_ids=GUILD_IDS)
    async def play(self, interaction: Interaction,
                   channel: GuildChannel = SlashOption(channel_types=[ChannelType.voice],
                                                       description="Voice channel to join"),
                   search: str = SlashOption(description="Search for a song")):

        if search.startswith("https://open.spotify.com/track/"):
            search = await spotify.SpotifyTrack.search(query=search, return_first=True)

        search = await wavelink.YouTubeTrack.search(query=search, return_first=True)

        if not interaction.guild.voice_client:
            vc: wavelink.Player = await channel.connect(cls=wavelink.Player)

        elif not getattr(interaction.user.voice, "channel", None):
            return await interaction.send("Join a voice channel and run this command again")
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        if vc.is_playing:
            print(vc.is_playing())
            vc.queue.put(search)
            await vc.play(search)
            await interaction.send(f"Now Playing: {search.title}")
        else:
            print(vc.is_playing())
            vc.queue.put(search)
            await interaction.send(f"Added {search.title} to queue")

        vc.interaction = interaction
        setattr(vc, "loop", False)
        if vc.loop:
            return

    @nextcord.slash_command(description="Pause the currently playing music", guild_ids=GUILD_IDS)
    async def pause(self, interaction: Interaction):
        if not interaction.guild.voice_client:
            return await interaction.send("If I'm not in a voice channel, then how am I going to pause music?")

        elif not getattr(interaction.user.voice, "channel", False):
            return await interaction.send("I'm not in a voice channel")

        else:
            vc: wavelink.Player = interaction.guild.voice_client

        await vc.pause()
        await interaction.send("Paused your music!")

    @nextcord.slash_command(description="resume paused music", guild_ids=GUILD_IDS)
    async def resume(self, interaction: Interaction):
        if not interaction.guild.voice_client:
            return await interaction.send("If I'm not in a voice channel, then how am I going to resume music?")

        elif not getattr(interaction.user.voice, "channel", False):
            return await interaction.send("I'm not in a voice channel")

        else:
            vc: wavelink.Player = interaction.guild.voice_client

        await vc.resume()
        await interaction.send("Resumed your music!")

    @nextcord.slash_command(description="Stops Currently playing music", guild_ids=GUILD_IDS)
    async def stop(self, interaction: Interaction):
        if not interaction.guild.voice_client:
            return await interaction.send("If I'm not in a voice channel, then how am I going to stop music?")

        elif not getattr(interaction.user.voice, "channel", False):
            return await interaction.send("I'm not in a voice channel")

        else:
            vc: wavelink.Player = interaction.guild.voice_client

        await vc.stop()
        await interaction.send("Stopped your music!")

    @nextcord.slash_command(description="removes bot from voice channel", guild_ids=GUILD_IDS)
    async def disconnect(self, interaction: Interaction):
        if not interaction.guild.voice_client:
            return await interaction.send("If I'm not in a voice channel, then how am I going to stop music?")

        elif not getattr(interaction.user.voice, "channel", False):
            return await interaction.send("I'm not in a voice channel")

        else:
            vc: wavelink.Player = interaction.guild.voice_client

        await vc.disconnect()
        await interaction.send("Bye!")

    @nextcord.slash_command(description="Loops playing music", guild_ids=GUILD_IDS)
    async def loop(self, interaction: Interaction):
        if not interaction.guild.voice_client:
            return await interaction.send("If I'm not in a voice channel, then how am I going to loop music?")

        elif not getattr(interaction.user.voice, "channel", False):
            return await interaction.send("I'm not in a voice channel")

        else:
            vc: wavelink.Player = interaction.guild.voice_client

        try:
            vc.loop ^= True
        except Exception:
            setattr(vc, "loop", False)

        if vc.loop:
            return await interaction.send("Loop Enabled!")

        else:
            return await interaction.send("Loop Disabled!")

    @nextcord.slash_command(description="Shows the current queue for the server", guild_ids=GUILD_IDS)
    async def queue(self, interaction: Interaction):
        if not interaction.guild.voice_client:
            return await interaction.send("Can't show the queue if I'm not in a voice chat")

        elif not getattr(interaction.user.voice, "channel", False):
            return await interaction.send("I'm not in a voice channel")

        else:
            vc: wavelink.Player = interaction.guild.voice_client

        if vc.queue.is_empty:
            return await interaction.send("Queue is empty")

        queue = vc.queue.copy()
        embed = queue_embed(interaction.guild.name, queue)

        await interaction.send(embed=embed)

    @nextcord.slash_command(description="Clears the queue", guild_ids=GUILD_IDS)
    async def clear(self, interaction: Interaction):
        if not interaction.guild.voice_client:
            return await interaction.send("Can't clear the queue if I'm not in a voice chat")

        elif not getattr(interaction.user.voice, "channel", False):
            return await interaction.send("You're not in a voice channel")

        else:
            vc: wavelink.Player = interaction.guild.voice_client

        if vc.queue.is_empty:
            return await interaction.send("No queue to clear")

        await vc.queue.clear
        return await interaction.send("The Queue has been cleared!")

def setup(bot: commands.Bot):
    bot.add_cog(Music(bot))
