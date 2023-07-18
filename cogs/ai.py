from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
import nextcord
from nextcord.ext import commands
from craiyon import Craiyon
from PIL import Image
import base64
from io import BytesIO
import time


class aiImageGen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="ai")
    async def ai(self, interaction):
        pass

    @ai.subcommand(name="generate", description="Generate an image with AI given a prompt")
    async def generate(self, interaction: Interaction,
                       prompt: str = SlashOption(description="Prompt for the AI to generate an image from")):
        # await interaction.response.defer()
        ETA = int(time.time()) + 60
        msg = await interaction.send(
            f"GO like do something productive while you wait for this to finish. ETA: <t:{ETA}:R>")
        generator = Craiyon()
        result = generator.generate(prompt)
        images = result.images
        for i in images:
            image = BytesIO(base64.decodebytes(i.encode("utf-8")))
            return await msg.edit(content="Here you go", file=nextcord.File(image, "image.png"))


def setup(bot):
    bot.add_cog(aiImageGen(bot))
