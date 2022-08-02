import nextcord
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption, ChannelType


class RoleView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def handle_click(self, button: nextcord.ui.Button, interaction: Interaction):
        role_id = 998069568805285979
        role = interaction.guild.get_role(role_id)
        assert isinstance(role, nextcord.Role)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.send("Event ping role has been removed", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.send("Event ping role has been added", ephemeral=True)

    @nextcord.ui.button(label="Event Ping", style=nextcord.ButtonStyle.green, custom_id="event_role_ping")
    async def event_button(self, button, interaction: Interaction):
        await self.handle_click(button, interaction)
