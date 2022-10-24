import discord, textwrap, ast
from discord.ext import commands
from datetime import datetime
from typing import List, cast

def cleanup_code(content: str) -> str:
	if content.startswith('```') and content.endswith('```'):
		return '\n'.join(content.split('\n')[1:])[:-3]
	else:
		return content

def insert_returns(body: List[ast.stmt]):
	if isinstance(body[-1], ast.Expr):
		body[-1] = ast.Return(body[-1].value)
		ast.fix_missing_locations(body[-1])

	if isinstance(body[-1], ast.If):
		insert_returns(body[-1].body)
		insert_returns(body[-1].orelse)

	if isinstance(body[-1], ast.With) or isinstance(body[-1], ast.AsyncWith):
		insert_returns(body[-1].body)

@commands.command(name='eval')
@commands.is_owner()
async def eval_cmd(ctx: commands.Context, *, cmd: str):
	cmd = cleanup_code(cmd)
	# env = {
	# 	"discord": discord,
	# 	"commands": commands,
	# 	"bot": ctx.bot,
	# 	"ctx": ctx,
	# 	"channel": ctx.channel,
	# 	"author": ctx.author,
	# 	"guild": ctx.guild,
	# 	"message": ctx.message
	# }

	# stdout = io.StringIO()

	# try:
	# 	with contextlib.redirect_stdout(stdout):
	# 		exec(
	# 			f"async def func():\n{textwrap.indent(code, '	')}", env
	# 		)

	# 		obj = await env["func"]()
	# 		result = f"{stdout.getvalue()}\n-- {obj}"
	# except Exception as e:
	# 	embed = discord.Embed(
	# 		colour=discord.Colour.dark_purple(),
	# 		title=f"❌ Eval Error: `{e.__class__.__name__}`",
	# 		description=f"```py\n{e}```",
	# 		timestamp=datetime.now()
	# 	)
	# 	return await ctx.reply(embed=embed)

	# embed = discord.Embed(
	# 	colour=discord.Colour.dark_purple(),
	# 	title="📜 Eval",
	# 	description=f"```py\n{result}```",
	# 	timestamp=datetime.now()
	# )

	# await ctx.reply(embed=embed)

	fn_name = "_eval_expr"

	body = f"async def {fn_name}():\n{textwrap.indent(cmd, '	')}"
	
	parsed = ast.parse(body)

	body = cast(ast.AsyncFunctionDef, parsed.body[0]).body
	insert_returns(body)

	env = {
		"discord": discord,
		"commands": commands,
		"bot": ctx.bot,
		"ctx": ctx,
		"channel": ctx.channel,
		"author": ctx.author,
		"guild": ctx.guild,
		"message": ctx.message
	}

	try:
		exec(compile(parsed, filename="<ast>", mode="exec"), env)

		result = await env["_eval_expr"]()

		embed = discord.Embed(
			colour=discord.Colour.dark_purple(),
			title="📜 Eval",
			description=f"```py\n{result}```",
			timestamp=datetime.now()
		)
		await ctx.reply(embed=embed)
	except Exception as e:
		embed = discord.Embed(
			colour=discord.Colour.dark_purple(),
			title=f"❌ Eval Error: `{e.__class__.__name__}`",
			description=f"```py\n{e}```",
			timestamp=datetime.now()
		)
		return await ctx.reply(embed=embed)

@eval_cmd.error
async def eval_error(ctx: commands.Context, error: commands.CommandError):
	if isinstance(error, commands.NotOwner):
		embed = discord.Embed(
			colour=discord.Colour.dark_purple(),
			title='❌ Error: `Not Owner`',
			description='```This command is limited to the bot developer(s).```'
		)
		return await ctx.reply(embed=embed)

	elif isinstance(error, commands.MissingRequiredArgument):
		embed = discord.Embed(
			colour=discord.Colour.dark_purple(),
			title='❌ Error: `Missing Argument`',
			description='```Please enter an expression/code to evaluate```'
		)
		return await ctx.reply(embed=embed)

	else:
		embed = discord.Embed(
			colour=discord.Colour.dark_purple(),
			title=f'❌ Error: `{error.__class__.__name__}`',
			description=f'```{error}```'
		)
		return await ctx.reply(embed=embed)

