import discord.ext.commands
import json

import catbot.config

class CatBotConfigNotLoadedError(Exception): pass

try:
    with open("catbot.json") as config_file:
        catbot.config.keys = json.load(config_file)
except FileNotFoundError:
    print("CatBot must be run from a folder containing a catbot.json file.")
    raise CatBotConfigNotLoadedError()
except json.JSONDecodeError as e:
    print("The catbot.json file must be in valid JSON format.")
    print(str(e))
    raise CatBotConfigNotLoadedError()
except TypeError as e:
    print("The catbot.json file must contain exactly one object with exactly two fields:")
    print("\t- \"discord\", containing the bot client token for your Discord application")
    print("\t- \"thecatapi\", containing the API key for your TheCatAPI.com account")
    print("Review the README file for this project if you don't know where to find these values.")
    raise CatBotConfigNotLoadedError()

catbot.config.get_headers = { "x-api-key": catbot.config.keys["thecatapi"] }
catbot.config.post_headers = { "x-api-key": catbot.config.keys["thecatapi"], "Content-Type": "application/json" } 

bot = discord.ext.commands.Bot(command_prefix=catbot.config.command_prefix)
