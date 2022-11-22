import discord
from datetime import datetime
from discord.ext import commands
from lib.utils import random_error
from lib.symbols import NBT
from lib.numbers import int_if_dotzero_float
from lib.calculations import parse_expr, Float, Integer

@commands.command(aliases=['calc'], description='Calculate an expression.')
@commands.cooldown(1, 5, commands.BucketType.user)
async def calculate(ctx: commands.Context, expression: str):
	res = int_if_dotzero_float(parse_expr(expression.replace('^', '**'), transformations='all'))
	embed = discord.Embed(
		colour=discord.Colour.dark_blue(),
		title=f'🧮 Calculation: `{expression}`'
	)
	if isinstance(res, Float) or isinstance(res, Integer):
		embed.description = f"```py\n‎\t{res}```"
		embed.timestamp = datetime.now()
		embed.timestamp = datetime.now()
		return await ctx.reply(embed=embed)
	elif isinstance(res, Exception):
		embed.title = random_error()
		embed.description = f"A code error occured:{NBT}*```py{res}```*"
		embed.timestamp = datetime.now()
		return await ctx.reply(embed=embed)

@calculate.error
async def calculate_error(ctx: commands.Context, error: commands.CommandError):
	if isinstance(error, commands.MissingRequiredArgument):
		embed = discord.Embed(
			colour=discord.Colour.dark_blue(),
			title=random_error(),
			description=f'Please enter an expression.{NBT}*(i.e. 1+2, 3*4...)*'
		)
		return await ctx.reply(embed=embed)