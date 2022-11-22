import discord, random
from discord.ext import commands
from lib.utils import random_error
from lib.symbols import NBT

@commands.command(name="8ball")
async def eight_ball(ctx: commands.Context, *, question: str):
	choices = [
		'Yes!',
		'No.',
		'Maybe?',
		'Probably..',
		'Probably not..',
		'Probably yes..',
		'...no',
		'Sure, I guess.',
		'Absolutely **no**.',
		'Absolutely **yes**.'
	]

	choice = random.choices(choices, k=1)[0]

	embed = discord.Embed(
		colour=discord.Colour.dark_blue(),
		title=f'🎱 The Magic Ball: `{question + "?" if not question.endswith("?") else question}`',
		description='*' + choice + '*'
	)

	await ctx.reply(embed=embed)

@eight_ball.error
async def eight_ball_error(ctx: commands.Context, error: commands.CommandError):
	if isinstance(error, commands.MissingRequiredArgument):
		embed = discord.Embed(
			colour=discord.Colour.dark_blue(),
			title=random_error(),
			description=f'Please enter a question.{NBT}*(i.e. Am I awesome? Are you intelligent...)*'
		)
		return await ctx.reply(embed=embed)