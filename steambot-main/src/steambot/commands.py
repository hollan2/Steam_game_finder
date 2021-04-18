from discord import Emoji, PartialEmoji
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
async def recat(ctx, emoji: Union[Emoji,PartialEmoji,str]):
    if emoji in steambot.config.reactions:
        catURL = steambot.config.imageURL.format(choice(steambot.config.reactions[emoji]))
        cat = requests.get(catURL, headers=steambot.config.get_headers).json()
        await ctx.send(cat["url"])
    else:
        await ctx.send("You haven't reacted to any cats with {}".format(emoji))
