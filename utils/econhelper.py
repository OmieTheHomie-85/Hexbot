import os, random
import nextcord
import asyncio
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption, ChannelType
import pymongo
from dotenv import load_dotenv
from pymongo import MongoClient
import os
from pymongo.errors import DuplicateKeyError, CursorNotFound
load_dotenv()
cluster = MongoClient(os.getenv("MONGO_URI"))
db = cluster["discord"]
collection = db["user"]

cards = ["5*", "4*", "3*"]


# Creates a document in database if one doesn't exist
async def create_balance(user):
    if collection.find_one({'_id': user.id}) is None:
        collection.insert_one({
            '_id': user.id,
            'name': user.name,
            'wallet': 0,
            'bank': 100,
            'cards': ["3*"]
        })


# Gets Balance of specified user
async def get_balance(user):
    result = collection.find_one({'_id': user.id})
    if result is None:
        await create_balance(user)
        return 0, 100, 500
    else:
        wallet, bank = result['wallet'], result['bank']
        return wallet, bank


# Updates the wallet
async def update_wallet(user, amount: int):
    result = collection.find_one({'_id': user.id})
    if result is None:
        await create_balance(user)
        return 0
    tot = result['wallet'] + amount
    print("Wallet: Tot is " + str(tot) + " it used to be " + str(result['wallet']))
    collection.update_one({'_id': user.id}, {'$set': {'wallet': tot}})


async def update_bank(user, amount: int):
    result = collection.find_one({'_id': user.id})
    if result is None:
        await create_balance(user)
        return 0
    tot = result['bank'] + amount
    print("Bank: Tot is " + str(tot) + " it used to be " + str(result['bank']))
    collection.update_one({'_id': user.id}, {'$set': {'bank': tot}})


async def get_inventory(user):
    result = collection.find_one({'_id': user.id})
    if result is None:
        await create_balance(user)
        return ['3*']

    else:
        cards = result['cards']
        return cards

async def give_inf(user):
    result = collection.find_one({'_id': user.id})
    if result is None:
        await create_balance(user)
        return 0

    collection.update_one({'_id': user.id}, {'$set': {'bank': 99999999999999999999}})



