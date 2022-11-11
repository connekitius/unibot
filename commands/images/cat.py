import requests, discord
from discord.ext import commands

@commands.command(aliases=['kitty', 'meow'])
async def cat(ctx: commands.Context):
	res = requests.get('https://aws.random.cat/meow').json()
	if res['file'] is not None:
		embed = discord.Embed(
			colour=discord.Colour.dark_blue(),
			title='🐈 Kitty Cats'
		)
		embed.set_image(url=res['file'])
		return await ctx.reply(embed=embed)
	else:
		embed = discord.Embed(
			colour=discord.Colour.dark_blue(),
			title='🐈❌ Kitty Cats Error',
			description='Could not load cat image(s).'
		)
		return await ctx.reply(embed=embed)