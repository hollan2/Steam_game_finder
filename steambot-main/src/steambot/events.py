from discord import User, Reaction
import discord.utils
import json
import requests

import steambot
import steambot.config

@steambot.bot.event
# Have to change all of these events:
async def on_ready():
    print("CatBot is running!")
    app_info = await steambot.bot.application_info()
    oauth_url = discord.utils.oauth_url(app_info.id, permissions=steambot.config.permissions)
    print("Use this URL to add CatBot to your Discord server:")
    print(oauth_url)

@steambot.bot.event
async def on_reaction_add(reaction: Reaction, user: User):
    emoji = reaction.emoji
    cat = steambot.config.cats[reaction.message.id]

    if cat is not None:
        if emoji in steambot.config.reactions:
            steambot.config.reactions[emoji].append(cat)
        else:
            steambot.config.reactions[emoji] = [cat]

        if emoji == steambot.config.vote_emoji:
            data = json.dumps({ "image_id": cat, "sub_id": "test", "value": 1 })
            vote = requests.post(steambot.config.voteURL, data=data, headers=steambot.config.post_headers)
            vote.raise_for_status()
            reply = "vote #{id} sent, server message: {message}".format(**vote.json())
            await reaction.message.channel.send(reply)
