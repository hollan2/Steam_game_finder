from discord import Emoji, PartialEmoji
from discord import ext
from random import choice
import requests
from typing import Union

import steambot
import steambot.config

@steambot.bot.command()
#Will need to change these commands:

# Thinking sign up command
# And Lets play command

async def cat(ctx):
    cat = requests.get(steambot.config.searchURL, headers=steambot.config.get_headers).json()[0]
    message = await ctx.send(cat["url"])
    steambot.config.cats[message.id] = cat["id"]
    print("cat:", cat["id"])

@steambot.bot.command()
async def start_party(ctx: ext.commands.Context):
    message = await ctx.send(f"{ctx.author} want's to play a game!"
                             f"React to this message to join a steam party!")
    steambot.config.events[message.id] = {}
