import nextcord
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption, ChannelType

from utils.EventAnnounceView import EventAnnounceView
from utils.RoleView import RoleView

GUILD_IDS = [847268531648462860]


class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self, ctx: commands.Context):
        self.bot.add_view(RoleView())
        self.bot.add_view(EventAnnounceView())

    @nextcord.slash_command(name="event", guild_ids=GUILD_IDS)
    async def event_role(self, interaction: Interaction):
        await interaction.send("Click a button to add or remove the **Event Ping** role", view=RoleView())

    @nextcord.slash_command(name="announce", description="Announce an Event")
    async def announce(self, interaction: Interaction, message):
        em = nextcord.Embed(title="Event Announcement", description=message)
        em.set_footer(text=f"Created by: {interaction.user}", icon_url=interaction.user.avatar.url)
        await interaction.send(embed=em)




def setup(bot: commands.Bot):
    bot.add_cog(Event(bot))
