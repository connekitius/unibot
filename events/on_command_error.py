from discord import Colour, Embed
from discord.ext.commands import CommandError, Context, errors

async def on_command_error(ctx: Context, error: CommandError):
	if isinstance(error, errors.CommandOnCooldown):
		embed = Embed(
			colour=Colour.dark_blue(),
			title=f'⏱ Not so fast buddy...`',
			description=f'Please wait `{round(error.retry_after, 2)}` {"seconds" if round(error.retry_after, 2) > 1 else "second"} to rerun *{ctx.command.name if ctx.command else "unknown"}*.'
		)
		return await ctx.reply(embed=embed)