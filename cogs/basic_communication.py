import discord

from discord.ext import commands

class BasicCommunication(commands.Cog, name='Events'):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.Cog.listener()
  async def on_ready(self):
    self.bot.owner = (await self.bot.application_info()).owner
    print('linus is ready')

  @commands.Cog.listener()
  async def on_message(self, message):
    if message.author == self.bot.user: return

def setup(bot):
  bot.add_cog(BasicCommunication(bot))