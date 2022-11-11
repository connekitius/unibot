import discord, requests, os, asyncio
from discord.ext import commands

@commands.command()
async def joke(ctx: commands.Context):
	endpoint = format(os.environ.get('JOKES_API_ENDPOINT'))
	res = requests.get(endpoint)
	json = res.json()
	if json['error'] is False or None:
		if json['type'] == 'single':
			content = json['joke']
			embed = discord.Embed(
				colour=discord.Colour.dark_blue(),
				title='😆 Jokes And Laughs',
				description=f'*{content}*'
			)
			embed.set_footer(text=f'Category: {json["category"]}')
			await ctx.reply(embed=embed)
		elif json['type'] == 'twopart':
			content = json['setup']
			embed = discord.Embed(
				colour=discord.Colour.dark_blue(),
				title='😆 Jokes And Laughs',
				description=f'**{content}**'
			)
			embed.set_footer(text=f'Category: {json["category"]}')
			m = await ctx.reply(embed=embed)
			await asyncio.sleep(5)
			embed.description = f'{embed.description}\n*{json["delivery"]}*'
			await m.edit(embed=embed)
		elif json['category'] == 'Pun':
			content = json['joke']
			embed = discord.Embed(
				colour=discord.Colour.dark_blue(),
				title='😏 Puns And Laughs',
				description=f'**{content}**'
			)
			embed.set_footer(text=f'Category: {json["category"]}')
			await ctx.reply(embed=embed)