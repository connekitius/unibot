import discord
from discord.ext import commands
from lib.utils import random_error
from lib.calculations import beautify_sympy, determine_sequence_type, get_nth_term, int_if_dotzero_float, sequence_types
from lib.symbols import NBT

@commands.group(invoke_without_command=True)
async def sequences(ctx: commands.Context, *, sequence: str):
	if not ',' in sequence:
		embed = discord.Embed(
			colour=discord.Colour.dark_blue(),
			title=random_error(),
			description=f'It seems you have not entered a valid sequence. Please enter a valid sequence seperated by commas.{NBT}*(i.e. 1, 2, 3, ...)*'
		)
		return await ctx.reply(embed=embed)

	terms = list(map(lambda s: int_if_dotzero_float(format(s).strip(' ')), sequence.split(',')))
	if len(terms) < 3:
		embed = discord.Embed(
			colour=discord.Colour.dark_blue(),
			title=random_error(),
			description=f'Please enter a sequence with at least 3 terms.{NBT}*(i.e. 1, 2, 3...)*'
		)
		return await ctx.reply(embed=embed)
	
	identifier = determine_sequence_type(terms)
	if identifier == sequence_types.unknown:
		embed = discord.Embed(
			colour=discord.Colour.dark_blue(),
			title=random_error(),
			description=f'Please enter a sequence of a known type.{NBT}*(known types: arithmetic, geometric, quadratic and fibonacci)*'
		)
		return await ctx.reply(embed=embed)

	nth = get_nth_term(terms, identifier)
	if nth is None:
		embed = discord.Embed(
			colour=discord.Colour.dark_blue(),
			title=random_error(),
			description=f'Please enter a valid sequence.{NBT}*(i.e. 1, 2, 3, ...)*'
		)
		return await ctx.reply(embed=embed)

	embed = discord.Embed(
		colour=discord.Colour.dark_blue(),
		title=f'#️⃣ Sequence Solver: `{", ".join(list(map(format, terms[:5])))}...`'
	)

	print(beautify_sympy(nth, identifier))
	embed.add_field(name='Nth Term', value=beautify_sympy(nth, identifier))
	embed.add_field(name='Type', value=identifier.name.capitalize())
	await ctx.reply(embed=embed)
