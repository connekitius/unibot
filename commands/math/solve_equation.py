import re, textwrap, discord
from typing import List, Literal
from sympy import Integer, Symbol, Eq, solve, Rational, sympify, Float
from sympy.parsing.sympy_parser import parse_expr, implicit_multiplication_application, standard_transformations
from discord.ext import commands
from datetime import datetime

transformations = (standard_transformations + (implicit_multiplication_application,))

def equate(string: str):
	string = string.lower().replace('^', '**')
	arr = re.findall("[a-z]", string)
	env = {
	    'solve': solve,
	    'Eq': Eq
	}
	if len(arr) > 0 and '=' in string:
		equation = str(parse_expr(string.split('=')[0], transformations=transformations))
		result = string.split('=')[1]
		for l in arr:
			env[l] = Symbol(l, real=True)
		funcdef = f"def _solve_equation():\n{textwrap.indent(f'return solve(Eq({equation}, {result}))', '   ')}"
		try:
			exec(funcdef, env)
			res = env['_solve_equation']()
			if isinstance(res, Rational):
				return f'{float(res)} ({res})'
			elif isinstance(res, List):
				if len(res) >= 2:
					return res
				else:
					if isinstance(res[0], Integer):
						return format(res[0])
					elif isinstance(res[0], Rational):
						return f'{Float(res[0])} ({res[0]})'
					else:
						return format(sympify(res[0]).evalf())
			else:
				return 0;
		except Exception as e:
			return e
	else:
		return 0;

@commands.command(aliases=['se'])
@commands.cooldown(1, 5.0)
async def solve_equation(ctx: commands.Context, equation: str):
	newLineChar = "\n"
	res = equate(equation)
	embed = discord.Embed(
		colour=discord.Colour.dark_purple(),
		title=f'➕ Equation Solving: `{equation}`'
	)
	if isinstance(res, str) or isinstance(res, type(Literal[0])):
		embed.description = f"```py\n‎\t{res}```"
		embed.timestamp = datetime.now()
		return await ctx.reply(embed=embed)
	elif isinstance(res, List):
		newList = list(map(lambda num: f'‎\t{num}', res))
		embed.description = f"```py\n{newLineChar.join(newList)}```"
		embed.timestamp = datetime.now()
		return await ctx.reply(embed=embed)
	elif isinstance(res, Exception):
		embed.title = f'❌ Solving Error: `{res.__class__.__name__}`'
		embed.description = f"```py\n‎\t{res}```"
		embed.timestamp = datetime.now()
		return await ctx.reply(embed=embed)

@solve_equation.error
async def solve_equation_error(ctx: commands.Context, error: commands.CommandError):
	if isinstance(error, commands.MissingRequiredArgument):
		embed = discord.Embed(
			colour=discord.Colour.dark_purple(),
			title='❌ Error: `Missing Argument`',
			description='```Please enter an equation.```'
		)
		return await ctx.reply(embed=embed)