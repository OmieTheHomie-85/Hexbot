import os
import nextcord
import asyncio
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
import pymongo
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, CursorNotFound
from utils.econhelper import *

GUILD_IDS = [847268531648462860]


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name='balance', description='Gets your or a specified users balance', guild_ids=GUILD_IDS)
    async def balance(self, interaction: Interaction, user: nextcord.Member = None):
        if user is None:
            user = interaction.user

        bank = await get_balance(user)
        em = nextcord.Embed(title=f"{user.name}'s Balance")
        em.add_field(name="wallet", value=bank[0])
        em.add_field(name="bank", value=f"{bank[1]}")
        inventory_em = nextcord.Embed(title=f"{user.name}'s Inventory")
        await interaction.send(embed=em)

    @nextcord.slash_command(name='give', description='Lets you give money to a specified user', guild_ids=GUILD_IDS)
    async def give(self, interaction: Interaction, user: nextcord.Member, amount: int = SlashOption(
        name="amount",
        description="Amount to give",
        required=True,
    )):
        if user == interaction.user:
            return await interaction.send("You can't give money to yourself /o")

        if amount < 0:
            return await interaction.send("I see what you're doing.... it just won't work.")

        reciver_bal = await get_balance(user)
        reciver_wallet = reciver_bal[0]

        sender_bal = await get_balance(interaction.user)
        sender_wallet = sender_bal[0]

        if amount > sender_wallet:
            return await interaction.send("You don't have enough money")

        await update_wallet(user, amount)
        await update_wallet(interaction.user, -amount)
        await interaction.send(f"{interaction.user.name} gave {amount}$ to {user.name}!")

    @nextcord.slash_command(name='withdraw', description='Lets you withdraw money from your bank', guild_ids=GUILD_IDS)
    async def withdraw(self, interaction: Interaction, amount: str = SlashOption(
        name="amount",
        description="Amount to withdraw",
        required=True,
    )):
        try:
            amount = int(amount)
        except ValueError:
            pass

        if type(amount) == str:
            if amount.lower() == "max" or amount.lower() == "all":
                amount = await get_balance(interaction.user)
                amount = amount[1]

        else:
            amount = int(amount)

        if amount < 0:
            return await interaction.send("I see what you're doing.... it just won't work.")

        bal = await get_balance(interaction.user)
        bank = bal[1]

        if amount > bank:
            return await interaction.send("You don't have enough money")

        bank_res = await update_wallet(interaction.user, amount)
        wallet_res = await update_bank(interaction.user, -amount)
        if bank_res == 0 or wallet_res == 0:
            return await interaction.send("Something went wrong")
        await interaction.send(f"{interaction.user.name} Withdrew {amount}$ from their bank!")

    @nextcord.slash_command(name='deposit', description='Lets you deposit money from your wallet', guild_ids=GUILD_IDS)
    async def deposit(self, interaction: Interaction, amount: str = SlashOption(
        name="amount",
        description="Amount to withdraw",
        required=True,
    )):
        try:
            amount = int(amount)
        except ValueError:
            pass

        if type(amount) == str:
            if amount.lower() == "max" or amount.lower() == "all":
                amount = await get_balance(interaction.user)
                amount = amount[0]

        else:
            amount = int(amount)

        if amount < 0:
            return await interaction.send("I see what you're doing.... it just won't work.")

        bal = await get_balance(interaction.user)
        wallet = bal[0]

        if amount > wallet:
            return await interaction.send("You don't have enough money")

        bank_res = await update_wallet(interaction.user, -amount)
        wallet_res = await update_bank(interaction.user, amount)
        if bank_res == 0 or wallet_res == 0:
            return await interaction.send("Something went wrong")
        await interaction.send(f"{interaction.user.name} deposited {amount}$ into their bank!")

def setup(bot: commands.Bot):
    bot.add_cog(Economy(bot))
