from discord import Emoji, PartialEmoji
from random import choice
import requests
from typing import Union

import catbot
import catbot.config

@catbot.bot.command()
async def cat(ctx):
    cat = requests.get(catbot.config.searchURL, headers=catbot.config.get_headers).json()[0]
    message = await ctx.send(cat["url"])
    catbot.config.cats[message.id] = cat["id"]
    print("cat:", cat["id"])

@catbot.bot.command()
async def recat(ctx, emoji: Union[Emoji,PartialEmoji,str]):
    if emoji in catbot.config.reactions:
        catURL = catbot.config.imageURL.format(choice(catbot.config.reactions[emoji]))
        cat = requests.get(catURL, headers=catbot.config.get_headers).json()
        await ctx.send(cat["url"])
    else:
        await ctx.send("You haven't reacted to any cats with {}".format(emoji))
