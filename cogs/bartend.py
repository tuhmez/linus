import discord
import json
import os

import asyncio
import aiohttp

from discord.ext import commands

class Bartend(commands.Cog, name='bartend', command_attrs=dict(hidden=False)):
  def __init__(self, bot):
    self.bot = bot

  randomUrl = 'https://www.thecocktaildb.com/api/json/v1/1/random.php'
  drinkNameUrl = 'https://www.thecocktaildb.com/api/json/v1/1/search.php?s='
  drinkIngredientUrl = 'https://www.thecocktaildb.com/api/json/v1/1/filter.php?i='
  drinkLandingUrl = 'https://www.thecocktaildb.com/drink.php?c='
  linusUrl = 'https://vignette.wikia.nocookie.net/himym/images/3/3e/Linus.jpg/revision/latest/scale-to-width-down/340?cb=20130925065354'

  async def fetch(self, session, url):
    async with session.get(url) as response:
      return await response.text()

  async def embed_drink(self, drinkName, drinkUrl, imageUrl, drinkDescription):
    embed = discord.Embed(title=drinkName, description=drinkDescription, url=drinkUrl)
    embed.set_author(name='linus', icon_url=self.linusUrl)
    embed.set_image(url=imageUrl)
    embed.set_footer(text='Courtesy of TheCocktailDB.com')
    return embed

  @commands.command(name='random', brief='Get a random drink!')
  async def get_random_drink(self, ctx):
    drink = None
    while True:
      async with aiohttp.ClientSession() as session:
        html = await self.fetch(session, self.randomUrl)
        drink = json.loads(html)['drinks'][0]

        if drink['strAlcoholic'] == 'Alcoholic': break

    drinkId = drink['idDrink']
    drinkName = drink['strDrink']
    drinkNameFormatted = drinkName.replace(' ', '-')
    url = f'{self.drinkLandingUrl}{drinkId}-{drinkNameFormatted}'
    drinkImage = drink['strDrinkThumb']

    drinkDescription = ''
    i = 1
    while i < 16:
      ingredientKey = f'strIngredient{i}'
      measureKey = f'strMeasure{i}'
      ingredient = drink[ingredientKey]
      measure = drink[measureKey]
      if ingredient is None: break
      if measure is None:
        drinkDescription += f'{ingredient}'
      else:
        drinkDescription += f'{measure} {ingredient}'
      if i < 15 and ingredient is not None: drinkDescription += '\n'
      i += 1
    embed = await self.embed_drink(drinkName, url, drinkImage, drinkDescription)
    await ctx.send(embed=embed)


  # @commands.command(name='ingredient', brief='Get drinks based on an ingredient!')
  # async def get_drink_by_ingredient(self, ctx, *, ingredient: str):
  #   async with aiohttp.ClientSession() as session:
  #     url = self.drinkIngredientUrl + ingredient
  #     html = await self.fetch(session, url)

  # async def main():
  #   async with aiohttp.ClientSession() as session:
  #     html = await fetch(session, 'https://www.thecocktaildb.com/api/json/v1/1/search.php?s=margarita')
  #     print(json.loads(html)['drinks'])
  #     for drink in json.loads(html)['drinks']:
  #       print(drink)

def setup(bot):
  bot.add_cog(Bartend(bot))