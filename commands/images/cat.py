import requests, discord, os
from discord.ext import commands
from lib.utils import random_error

@commands.command(aliases=['kitty', 'meow'])
async def cat(ctx: commands.Context):
	endpoint = format(os.environ.get('CATS_API_ENDPOINT'))
	res = requests.get(endpoint).json()
	if res['file'] is not None:
		embed = discord.Embed(
			colour=discord.Colour.dark_blue(),
			title='🐈 Kitties and Cats'
		)
		embed.set_image(url=res['file'])
		return await ctx.reply(embed=embed)
	else:
		embed = discord.Embed(
			colour=discord.Colour.dark_blue(),
			title=random_error(),
			description='Could not load cat image(s).'
		)
		return await ctx.reply(embed=embed)