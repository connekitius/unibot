import discord, wikipedia, re
from typing import List
from discord.ext import commands

NEWLINE = '\n'
@commands.group(name='wikipedia', invoke_without_command=True)
async def wikipedia_cmd(ctx: commands.Context):
	pass

@wikipedia_cmd.command()
async def search(ctx: commands.Context, *, query: str):
	embed = discord.Embed(
		colour=discord.Colour.dark_blue(),
		title='🌐 Wikipedia - Search',
		description='Searching for your topic...'
	)
	m = await ctx.reply(embed=embed)
	res = wikipedia.search(query.lower())
	if isinstance(res, List) and len(res) > 0:
		mapped = list(map(lambda s: '‎\t' + format(s), res))
		embed.description = f"**Found topics:**{NEWLINE}	{NEWLINE.join(mapped)}"
		embed.set_footer(text=f'{len(res)} Results')
		await m.edit(embed=embed)
	else:
		embed.description = f'No topics regarding `{query}` were found.'
		embed.set_footer(text='0 Results')
		await m.edit(embed=embed)

@wikipedia_cmd.command()
async def view(ctx: commands.Context, *, page: str):
	embed = discord.Embed(
		colour=discord.Colour.dark_blue(),
		title='🌐 Wikipedia - View',
		description='Searching for your page...'
	)
	m = await ctx.reply(embed=embed)

	try:
		wiki_page = wikipedia.page(title=page.lower())
		embed = discord.Embed(
			colour=discord.Colour.dark_purple(),
			title=f'🌐 Wikipedia - View: `{wiki_page.title}`',
			description=re.sub(r'\.(?=[^ \W\d])', f'.{NEWLINE}', wiki_page.summary)
		)

		if wiki_page.images[0]:
			embed.set_thumbnail(url=wiki_page.images[0])

		if wiki_page.categories:
			embed.set_footer(text=f'Categories: {", ".join(wiki_page.categories[:25]) if len(wiki_page.categories) >= 25 else ", ".join(wiki_page.categories)} {" and more..." if len(wiki_page.categories) else ""}')

		if wiki_page.url:
			embed.url = wiki_page.url

		return await m.edit(embed=embed)

	except Exception as e:
		if isinstance(e, wikipedia.PageError):
			embed = discord.Embed(
				colour=discord.Colour.dark_blue(),
				title='🌐 Wikipedia - View',
				description=f'No pages regarding `{page}` were found.'
			)
			return await m.edit(embed=embed)
