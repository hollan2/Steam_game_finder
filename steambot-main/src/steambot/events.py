from discord import User, Reaction
import discord.utils
import json
import requests

import steambot
import steambot.config

@steambot.bot.event
# Have to change all of these events:
async def on_ready():
    print("steambot is running!")
    app_info = await steambot.bot.application_info()
    oauth_url = discord.utils.oauth_url(app_info.id, permissions=steambot.config.permissions)
    print("Use this URL to add steambot to your Discord server:")
    print(oauth_url)

@steambot.bot.event
async def on_reaction_add(reaction: Reaction, user: User):
    if reaction.message.id in steambot.config.events:
        party = steambot.config.events[reaction.message.id]
        if user.bot:
            await reaction.message.channel.send(f"Sorry {user.name}, "
                                                f"this adventure is for "
                                                f"humans only")
        party[user.id] = user.name
        await reaction.message.channel.send(f"{user.name} has joined the "
                                            f"party!")

@steambot.bot.event
async def on_reaction_remove(reaction: Reaction, user: User):
    if reaction.message.id in steambot.config.events:
        party = steambot.config.events[reaction.message.id]
        if user.id in party.keys():
            party.pop(user.id, None)
            await reaction.message.channel.send(f"{user.name} has left the "
                                                f"party!")
