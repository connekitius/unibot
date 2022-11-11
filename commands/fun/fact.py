import discord, requests, os
from discord.ext import commands

@commands.command()
async def fact(ctx: commands.Context):
	endpoint = format(os.environ.get('FACTS_API_ENDPOINT'))
	res = requests.get(endpoint)
	content = res.json()['text']
	if content:
		embed = discord.Embed(
			colour=discord.Colour.dark_blue(),
			title='❓ Fact',
			description=f'*{content}*'
		)
		await ctx.reply(embed=embed)
	else:
		while content is None or not isinstance(content, str):
			content = requests.get(endpoint).json()['text']
		embed = discord.Embed(
			colour=discord.Colour.dark_blue(),
			title='❓ Fact',
			description=f'*{content}*'
		)
		await ctx.reply(embed=embed)