from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
import nextcord
from nextcord.ext import commands, activities

class Activities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @nextcord.slash_command(name="activity", description="play games with bot")
    # def activity(self, interaction,  channel: nextcord.VoiceChannel, game: activities.Activity.name = SlashOption(description="Activity to play")):
    #     invite_link = await channel.create_activity_invite(activities.Activity.chess)

def setup(bot):
    bot.add_cog(Activities(bot))
