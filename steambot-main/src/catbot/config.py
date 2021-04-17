import discord

command_prefix = '!'

vote_emoji = '👍'

permissions = discord.Permissions(
    send_messages=True,
    embed_links=True,
)

searchURL = "https://api.thecatapi.com/v1/images/search"
imageURL  = "https://api.thecatapi.com/v1/images/{}"
voteURL   = "https://api.thecatapi.com/v1/votes"

get_headers = None
post_headers = None

cats = {}
reactions = {}

keys = None
