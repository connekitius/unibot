from typing import Optional, cast
import discord
from discord.ext import commands

statuses = {
	'offline': 'ā«',
	'online': 'š¢',
	'dnd': 'š“',
	'idle': 'š”'
}

@commands.command(description='Check your profile and mutual servers with bot.')
async def profile(ctx: commands.Context, member: Optional[discord.Member] = None):
	user = member or cast(discord.Member, ctx.author)
	activity = "N/A" if user.activity == None else f"{cast(discord.CustomActivity, user.activity).emoji} {cast(discord.CustomActivity, user.activity).name}"
	embed = discord.Embed(
		colour=discord.Colour.dark_blue(),
		title=f'š Profile: `{user.display_name}` [{"š±" if user.is_on_mobile() else "š»"}]',
		description=f'*{activity}*'
	).set_thumbnail(
		url=user.display_avatar.url
	).add_field(
		name='User Info', value=f'ā\t__ID__: `{user.id}`\nā\t__Tag__: `{user.name}#{user.discriminator}`\nā\t__Status__: {format(user.status.value).capitalize()} {statuses.get(format(user.status.value))}'
	).add_field(
		name='Top Role', value='ā\t' + user.top_role.mention
	).add_field(
		name='Is Guild Owner', value='ā\t' + ("ā" if user.id != user.guild.owner_id else 'ā')
	)

	if user.id != ctx.me.id:
		embed.add_field(
			name='Mutual Guilds', value='ā\t' + '\nā\t'.join(map(lambda g: f'`{g.name}`', user.mutual_guilds))
		)

	await ctx.reply(embed=embed)