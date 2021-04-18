from discord import Emoji, PartialEmoji
from discord import ext
from random import choice
import requests
from typing import Union
from . import database

import steambot
import steambot.config

import steam.steamid

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

@steambot.bot.command()
async def debug(ctx: ext.commands.Context):
    await ctx.send(database.db)

@steambot.bot.command()
async def enroll(ctx: ext.commands.Context, username: str):
    #steamId = steam.steamid.SteamID(username)
    #if not steamId.is_valid():

    if username.isdigit():
        url = f"https://steamcommunity.com/profiles/{username}"
    else:
        url = f"https://steamcommunity.com/id/{username}"

    id64 = steam.steamid.steam64_from_url(url, http_timeout=30)
    if id64 is None:
        await ctx.send(f"Hey {ctx.message.author.name}, "
                        f"the provided steam id {username} "
                        f"is invalid")
        return

    database.db['usernames'][ctx.message.author.id] = id64
    database.save_db()
    await ctx.send(f"Hey {ctx.message.author.name}, "
			f"thanks for signing up to Steam Game Finder "
			f"with your username: {username}! :D")

@steambot.bot.command()
async def unenroll(ctx: ext.commands.Context):
    database.db['usernames'].pop(ctx.message.author.id, None)
    database.save_db()
    await ctx.send(f"Hey {ctx.message.author.name}, "
			f"you have been unenrolled! ")
