import requests, discord, os
from discord.ext import commands
from lib.utils import random_error

@commands.command()
async def fox(ctx: commands.Context):
	endpoint = format(os.environ.get('FOXES_API_ENDPOINT'))
	res = requests.get(endpoint).json()
	if res['image']:
		embed = discord.Embed(
			colour=discord.Colour.dark_blue(),
			title='🦊 Foxes'
		)
		embed.set_image(url=res['image'])
		return await ctx.reply(embed=embed)
	else:
		embed = discord.Embed(
			colour=discord.Colour.dark_blue(),
			title=random_error(),
			description='Could not load fox image(s).'
		)
		return await ctx.reply(embed=embed)