from discord import Emoji, PartialEmoji
from discord import ext
from random import choice
import requests
from typing import Union
from . import database

import steambot
import steambot.config


async def cat(ctx):
    cat = requests.get(steambot.config.searchURL, headers=steambot.config.get_headers).json()[0]
    message = await ctx.send(cat["url"])
    steambot.config.cats[message.id] = cat["id"]
    print("cat:", cat["id"])

@steambot.bot.command()
async def start_party(ctx: ext.commands.Context):
    message = await ctx.send(f"{ctx.author} want's to play a game! "
                             f"React to this message to join a steam party!")
    database.db['parties'][message.id] = {}
    database.save_db()

async def debug(ctx: ext.commands.Context):
    await ctx.send(database.db)
    steambot.config.events[message.id] = {}

@steambot.bot.command()
async def enroll_user(ctx, username):
    steambot.config.usernames[user.id] = username
    await ctx.send("Thanks for signing up :D")
