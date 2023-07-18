import os
import nextcord
import asyncio
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
import aiohttp
import openai

SECRET_KEY ="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"

class ChatGPT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name='chat', description='Use CHATGPT to cheat on your school assingments')
    async def chat(self, interaction, prompt: str):
        await interaction.response.defer()
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": "text-davinci-003",
                "prompt": prompt,
                "temperature": 0.5,
                "max_tokens": 50,
                "presence_penalty": 0,
                "best_of": 1,
            }

            headers = {"Authorization": f"Bearer {SECRET_KEY}"}
            async with session.post("https://api.openai.com/v1/completions", json=payload, headers=headers) as resp:
                data = await resp.json()
                embed = nextcord.Embed(title=f"Response to: {prompt}", description={data["choices"][0]["text"]})
                await interaction.followup.send(embed=embed)


def setup(bot):
    bot.add_cog(ChatGPT(bot))
