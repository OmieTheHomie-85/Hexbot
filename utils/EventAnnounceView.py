import nextcord
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption, ChannelType

class EventAnnounceView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

