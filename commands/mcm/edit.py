import subprocess, discord, os
from discord.ext import commands

@commands.command()
@commands.is_owner()
async def edit(ctx: commands.Context):
	paintPath = "C:\\Windows\\system32\\mspaint.exe"
	picturePath = os.path.abspath('./drawing.png')
	subprocess.Popen([paintPath, picturePath])
	await ctx.reply('Opened MCM picture.')

@edit.error
async def edit_error(ctx: commands.Context, error: commands.CommandError):
	if isinstance(error, commands.NotOwner):
		embed = discord.Embed(
			colour=discord.Colour.dark_purple(),
			title='❌ Error: `Not Owner`',
			description='```This command is limited to the bot developer(s).```'
		)
		return await ctx.reply(embed=embed)