import discord
import json
import os

from discord.ext import commands
from os import listdir
from os.path import isfile, join

with open('./config/config.json') as f:
  config = json.load(f)
  token = config["token"]

bot = commands.Bot(command_prefix='-')
cogs = [f for f in listdir('./cogs') if isfile(join('./cogs', f))]
for index, item in enumerate(cogs):
  cogs[index] = "cogs." + cogs[index].replace(".py", "")

if __name__ == '__main__':
  for cog in cogs:
    try:
      bot.load_extension(cog)
    except Exception as error:
      print(f'Cog {cog} cannot be loaded. [{error}]')

  bot.run(token)