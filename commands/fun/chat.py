import requests, discord, os
from discord.ext import commands
from lib.utils import random_error
from lib.symbols import NBT

@commands.command()
async def chat(ctx: commands.Context, *, message: str):
	brainId = format(os.environ.get('CHATBOT_BRAIN_ID'))
	apiKey = format(os.environ.get('CHATBOT_API_KEY'))
	res = requests.get(f'http://api.brainshop.ai/get?bid={brainId}&key={apiKey}&uid={ctx.author.id}&msg={message}')
	content = res.json()['cnt']
	embed = discord.Embed(
		colour=discord.Colour.dark_blue(),
		title='🤖 Chatbot',
		description=f'*{content}*'
	)
	await ctx.reply(embed=embed)

@chat.error
async def chat_error(ctx: commands.Context, error: commands.CommandError):
	if isinstance(error, commands.MissingRequiredArgument):
		embed = discord.Embed(
			colour=discord.Colour.dark_blue(),
			title=random_error(),
			description=f'Please enter a message.{NBT}*(i.e. Hi! How are you...)*'
		)
		return await ctx.reply(embed=embed)