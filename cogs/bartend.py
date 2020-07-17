import discord
import json
import os

import asyncio
import aiohttp

from discord.ext import commands

randomUrl = 'https://www.thecocktaildb.com/api/json/v1/1/random.php'
drinkNameUrl = 'https://www.thecocktaildb.com/api/json/v1/1/search.php?s='
drinkIngredientUrl = 'https://www.thecocktaildb.com/api/json/v1/1/filter.php?i='
drinkLandingUrl = 'https://www.thecocktaildb.com/drink.php?c='

async def fetch(session, url):
  async with session.get(url) as response:
    return await response.text()

async def embed_drink(drinkName, drinkUrl, imageUrl, drinkDescription):
  embed = discord.Embed(title=drinkName, description=drinkDescription, url=drinkUrl)
  embed.set_author(name='linus', icon_url='shorturl.at/stHU0')
  embed.set_image(url=imageUrl)
  embed.set_footer(text='Courtesy of TheCocktailDB.com')
  return embed

@command.command(name='random', brief='Get a random drink!')
async def get_random_drink(self, ctx):
  async with aiohttp.ClientSession() as session:
    html = await fetch(session, randomUrl)
    drink = json.loads(html)['drinks'][0]

    drinkId = drink['idDrink']
    drinkName = drink['strDrink']
    drinkNameFormatted = drinkName.replace(' ', '-')
    url = f'{drinkLandingUrl}{drinkId}-{drinknameFormatted}'
    drinkImage = drink['strDrinkThumb']

    drinkDescription = ''
    i = 0
    while i < 15:
      ingredientKey = f'strIngredient{i}'
      measureKey = f'strMeasure{i}'
      ingredient = drink[ingredientKey]
      measure = drink[measureKey]
      if ingredient is None: return
      drinkDescription += f'{measure} {ingredient}'
      if i > 14: drinkDescription += ',\n'
      i += 1
    embed = await embed_drink(drinkName, url, drinkImage)
    await ctx.send(embed=embed)


@command.command(name='ingredient', brief='Get drinks based on an ingredient!')
async def get_drink_by_ingredient(self, ctx, *, ingredient: str):
  async with aiohttp.ClientSession() as session:
    url = drinkIngredientUrl + ingredient
    html = await fetch(session, url)

async def main():
  async with aiohttp.ClientSession() as session:
    html = await fetch(session, 'https://www.thecocktaildb.com/api/json/v1/1/search.php?s=margarita')
    print(json.loads(html)['drinks'])
    for drink in json.loads(html)['drinks']:
      print(drink)

# if __name__ == '__main__':
#   loop = asyncio.get_event_loop()
#   loop.run_until_complete(main())