import glob, discord, os
from typing import Dict, List, Union
from discord.ext import commands

def returnInline(prim_str: str, strs = None) -> str:
	if strs != None:
		arr = list(strs)
		arr.append(prim_str)
		def returnInlineSingular(string: str):
			return f'`{string}`'

		return returnInlineSingular(' '.join(list(map(format, arr))))
	else:
		return f'`{prim_str}`'

@commands.command(aliases=['h'], description='View information about all commands or a specific command.', extras={
	'examples': ['$$help', '$$h', '$$help ping']
})
async def help(ctx: commands.Context, cmd_name: Union[str, None] = None):
	bot: commands.Bot = ctx.bot
	if cmd_name == None:
		catDir: Dict[str, List[str]] = {}
		for file in glob.glob('./commands/**/*.py', recursive=True):
			cmdName = os.path.basename(file).split('.')[0]
			if not cmdName.startswith('_'):
				fldrName = os.path.basename(os.path.dirname(file))
				if fldrName not in list(catDir.keys()):
					catDir[fldrName] = []

				catDir[fldrName].append(cmdName)
			else:
				continue

		embed = discord.Embed(
			colour=discord.Colour.dark_blue(),
			title='ℹ Unibot Help Prompt',
			description="Welcome to Unibot.\nUnibot is an open-sourced Python Discord bot built as a means of educational demonstration for the capabilities of Python as a programming language and in terms of functionality.\nThis prompt will show you all available commands as well as their categories.\nAs for command arguments, `<...>` implies a required argument, while `[...]` implies an optional argument.\nFor more information regarding a command, please run `$$help` with the command name."
		)

		for k in catDir:
			embed.add_field(name=k.capitalize(), value=' | '.join(list(map(returnInline, catDir[k]))), inline=True)

		await ctx.reply(embed=embed)
	elif cmd_name != None:
		cmd = bot.get_command(cmd_name.lower())
		if cmd == None:
			embed = discord.Embed(
				colour=discord.Colour.dark_blue(),
				description=f'Command `{cmd_name.lower()}` does not exist.'
			)
			return await ctx.reply(embed=embed)

		title = f'{cmd.name}'
		if cmd.cooldown:
			title += f' [⏲ {format(cmd.cooldown.per)}s]'

		helpEmbed = discord.Embed(
			colour=discord.Colour.dark_blue(),
			title=title
		)

		if cmd.description:
			helpEmbed.description = f'*{cmd.description}*'
		else:
			helpEmbed.description = '*N/A (no description provided)*'

		if cmd.aliases:
			helpEmbed.add_field(name='Aliases', value=', '.join(map(returnInline, cmd.aliases)), inline=False)
		elif cmd.extras.get('examples') != None:
			helpEmbed.add_field(name='Examples', value='\n'.join(map(returnInline, cmd.extras['examples'])), inline=False)

		await ctx.reply(embed=helpEmbed)