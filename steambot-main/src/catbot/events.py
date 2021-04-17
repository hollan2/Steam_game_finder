from discord import User, Reaction
import discord.utils
import json
import requests

import catbot
import catbot.config

@catbot.bot.event
async def on_ready():
    print("CatBot is running!")
    app_info = await catbot.bot.application_info()
    oauth_url = discord.utils.oauth_url(app_info.id, permissions=catbot.config.permissions)
    print("Use this URL to add CatBot to your Discord server:")
    print(oauth_url)

@catbot.bot.event
async def on_reaction_add(reaction: Reaction, user: User):
    emoji = reaction.emoji
    cat = catbot.config.cats[reaction.message.id]

    if cat is not None:
        if emoji in catbot.config.reactions:
            catbot.config.reactions[emoji].append(cat)
        else:
            catbot.config.reactions[emoji] = [cat]

        if emoji == catbot.config.vote_emoji:
            data = json.dumps({ "image_id": cat, "sub_id": "test", "value": 1 })
            vote = requests.post(catbot.config.voteURL, data=data, headers=catbot.config.post_headers)
            vote.raise_for_status()
            reply = "vote #{id} sent, server message: {message}".format(**vote.json())
            await reaction.message.channel.send(reply)
