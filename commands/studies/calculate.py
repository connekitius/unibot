from sympy import Integer, Float
from sympy.parsing.sympy_parser import parse_expr, implicit_multiplication_application, standard_transformations
from discord.ext import commands
from datetime import datetime
import discord

transformations = (standard_transformations + (implicit_multiplication_application,))

def is_int(n):
	try:
		float_n = float(n)
		int_n = int(float_n)
	except ValueError:
		return False
	else:
		return float_n == int_n

def is_float(n):
	try:
		float(n)
	except ValueError:
		return False
	else:
		return True

@commands.command(aliases=['calc'], description='Calculate an expression.')
@commands.cooldown(1, 5.0)
async def calculate(ctx: commands.Context, expression: str):
	res = parse_expr(expression.replace('^', '**'), transformations=transformations)
	res = Integer(Float(res)) if is_int(res) else Float(res) if is_float(res) else res
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
		embed.title = f'❌ Calculation Error: `{res.__class__.__name__}`'
		embed.description = f"```py\n‎\t{res}```"
		embed.timestamp = datetime.now()
		return await ctx.reply(embed=embed)

@calculate.error
async def calculate_error(ctx: commands.Context, error: commands.CommandError):
	if isinstance(error, commands.MissingRequiredArgument):
		embed = discord.Embed(
			colour=discord.Colour.dark_blue(),
			title='❌ Error: `Missing Argument`',
			description='```Please enter an expression.```'
		)
		return await ctx.reply(embed=embed)