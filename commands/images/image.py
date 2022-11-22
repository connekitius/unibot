import os, json, random, discord
from discord.ext import commands
from urllib import request as req, parse
from lib.utils import random_error
CGS_PID = os.environ.get('GOOGLE_SEARCH_CX')
CGS_API_KEY = os.environ.get('GOOGLE_SEARCH_API_KEY')

class NoResultsError(ValueError):
	def __str__(self) -> str:
		return 'No results were found.'

def get_random_image(query: str):
	if CGS_PID is None or CGS_API_KEY is None:
		return

	q = parse.quote_plus(query)

	request = req.Request(
	    'https://www.googleapis.com/customsearch/v1?key=' + CGS_API_KEY + '&cx=' +
	    CGS_PID + '&q=' + q + '&searchType=image&safe=high')

	with req.urlopen(request) as f:
		data = f.read().decode('utf-8')
	    
	data = json.loads(data)
	results = data['items']
	if len(results) >= 1:
		return format(random.choice(results)['link'])
	else:
		raise NoResultsError()

@commands.command()
@commands.cooldown(1, 20, commands.BucketType.user)
async def image(ctx: commands.Context, *, query: str):
	try:
		starter = discord.Embed(
			colour=discord.Colour.dark_blue(),
			title=f'🖼🔍 Image Search: `{query.lower()}`',
			description='Searching...'
		)
		m = await ctx.reply(embed=starter)
		url = get_random_image(query)
		starter.description = None
		starter.set_image(url=url)
		await m.edit(embed=starter)
	except Exception as e:
		if isinstance(e, NoResultsError):
			embed = discord.Embed(
				colour=discord.Colour.dark_blue(),
				title=random_error(),
				description=e.__str__()
			)
			return await ctx.reply(embed=embed)
