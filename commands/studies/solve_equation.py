import discord
from discord.ext import commands
from datetime import datetime
from lib.utils import random_error
from lib.calculations import equate, List
from lib.symbols import NBT, NEWLINE
from typing import Literal

@commands.command(aliases=['se'], description='Solve an equation.')
@commands.cooldown(1, 5, commands.BucketType.user)
async def solve_equation(ctx: commands.Context, equation: str):
	res = equate(equation)
	embed = discord.Embed(
		colour=discord.Colour.dark_blue(),
		title=f'➕ Equation Solving: `{equation}`'
	)
	if isinstance(res, str) or isinstance(res, type(Literal[0])):
		embed.description = f"```py\n‎\t{res}```"
		embed.timestamp = datetime.now()
		return await ctx.reply(embed=embed)
	elif isinstance(res, List):
		newList = list(map(lambda num: f'‎\t{num}', res))
		embed.description = f"```py\n{NEWLINE.join(newList)}```"
		embed.timestamp = datetime.now()
		return await ctx.reply(embed=embed)
	elif isinstance(res, Exception):
		embed.title = random_error()
		embed.description = f"```py\n‎\t{res}```"
		embed.timestamp = datetime.now()
		return await ctx.reply(embed=embed)

@solve_equation.error
async def solve_equation_error(ctx: commands.Context, error: commands.CommandError):
	if isinstance(error, commands.MissingRequiredArgument):
		embed = discord.Embed(
			colour=discord.Colour.dark_blue(),
			title=random_error(),
			description=f'Please enter an equation.{NBT}*(i.e. 2x+4=10, 6x=10-2x...)*'
		)
		return await ctx.reply(embed=embed)