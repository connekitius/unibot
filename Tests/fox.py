import requests
import discord
from discord.ext import commands

url = "randomfox.ca/floof"
@commands.command(aliases=["fox", "foxy"])
async def cat(ctx: commands.Context):
	res = requests.get(url).json()
	if res['file'] is not None:
		embed = discord.Embed(
			colour=discord.Colour.dark_blue(),
			title='🦊 Foxy fox'
		)
		embed.set_image(url=res['file'])
		return await ctx.reply(embed=embed)
	else:
		embed = discord.Embed(
			colour=discord.Colour.dark_blue(),
			title='🦊❌ Foxy fox Error',
			description='Could not load Fox image(s).'
		)
		return await ctx.reply(embed=embed)
