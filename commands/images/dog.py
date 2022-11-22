import requests, discord, os
from discord.ext import commands
from lib.utils import random_error

@commands.command(aliases=['puppy', 'bark'])
async def dog(ctx: commands.Context):
	endpoint = format(os.environ.get('DOGS_API_ENDPOINT'))
	res = requests.get(endpoint).json()
	if res['status'] == "success":
		embed = discord.Embed(
			colour=discord.Colour.dark_blue(),
			title='🐕 Puppies and Dogs'
		)
		embed.set_image(url=res['file'])
		return await ctx.reply(embed=embed)
	else:
		embed = discord.Embed(
			colour=discord.Colour.dark_blue(),
			title=random_error(),
			description='Could not load dog image(s).'
		)
		return await ctx.reply(embed=embed)