import discord.ext.commands
import json

import steambot.config

class SteamBotConfigNotLoadedError(Exception): pass

try:
    with open("steambot.json") as config_file:
        steambot.config.keys = json.load(config_file)
except FileNotFoundError:
    print("Steam Bot must be run from a folder containing a steambot.json file.")
    raise SteamBotConfigNotLoadedError()
except json.JSONDecodeError as e:
    print("The steambot.json file must be in valid JSON format.")
    print(str(e))
    raise SteamBotConfigNotLoadedError()
except TypeError as e:
    print("The steambot.json file must contain exactly one object with exactly two fields:")
    print("\t- \"discord\", containing the bot client token for your Discord application")
#change these probs
    print("\t- \"thecatapi\", containing the API key for your TheCatAPI.com account")
    print("Review the README file for this project if you don't know where to find these values.")
    raise SteamBotConfigNotLoadedError()

steambot.config.get_headers = { "x-api-key": steambot.config.keys["thecatapi"] } #insert steam api in the quotations
steambot.config.post_headers = { "x-api-key": steambot.config.keys["thecatapi"], "Content-Type": "application/json" } #insert steam api in the quotations

bot = discord.ext.commands.Bot(command_prefix=steambot.config.command_prefix)
