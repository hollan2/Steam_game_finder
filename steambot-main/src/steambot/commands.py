from discord import Emoji, PartialEmoji
from discord import ext
from random import choice
import requests
from typing import Union
from . import database

import steambot
import steambot.config

import steam.steamid

from . import steam_api

import json

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

@steambot.bot.command()
async def get_list(ctx: ext.commands.Context):
    games = steam_api.compare_games("", database.db['usernames'].values()) 
    games_info = {g: steam_api.get_game_info("", g) for g in games.keys()}
    no_info_games = {k:v for k,v in games_info.items() if v == {}}
    for key in no_info_games:
        games.pop(key)
        games_info.pop(key)

    multiplayer_games = {appid: games[appid] for appid in games.keys() if steam_api.is_game_multiplayer(appid, games_info)}
    games_with_metacritic = steam_api.add_metacritic(multiplayer_games, games_info)
    message = steam_api.get_best_games(games_with_metacritic)
    await ctx.send(message)
    
