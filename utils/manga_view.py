import nextcord
from nextcord.ext import commands
from nextcord import Interaction


class MangaView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def handle_click(self, button: nextcord.ui.Button, interaction: Interaction):
        await interaction.message.edit(content="p2")

    @nextcord.ui.button(label="go forward", style=nextcord.ButtonStyle.green)
    async def forward_button(self, button, interaction: Interaction):
        await self.handle_click(button, interaction)
