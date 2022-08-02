from multiprocessing.dummy import Array
import nextcord
from nextcord.ext import commands
from typing import Optional


def greenEmbed(title, description: Optional[str]) -> nextcord.Embed:
    """
    Makes an embed for commands that worked
    """
    wembed = nextcord.Embed(title=f'✅  {title}', description=description, color=0x2ecc71)

    return wembed


def redEmbed(title, description: Optional[str]) -> nextcord.Embed:
    """
    Makes an embed for commands that didn't work
    """
    bembed = nextcord.Embed(title=f'❌  {title}', description=description, color=0xe74c3c)

    return bembed


def queue_embed(guild, queue_array) -> nextcord.Embed:
    """
    Makes an embed for queue
    """
    QueueEmbed = nextcord.Embed(title="Queue", description=f'queue for {guild}', color=0x2ecc71)
    song_count = 0
    for song in queue_array:
        song_count += 1
        QueueEmbed.add_field(name=f'{song_count}. {song.title}', value=f'This the #{song_count} in the queue',
                             inline=False)
    return QueueEmbed
