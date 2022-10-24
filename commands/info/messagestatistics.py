import discord
from discord.ext import commands
from typing import Optional, cast

@commands.command(aliases=['ms'])
@commands.cooldown(1, 20.0)
async def messagestatistics(ctx: commands.Context, member: Optional[discord.Member] = None):
	user = member or ctx.author
	if ctx.guild == None or ctx.channel.type == discord.DMChannel.type:
		return;

	m = await ctx.reply('🔃 Loading...')
	channelMsgsList = [messages async for messages in ctx.channel.history(limit=10000)]
	channelMsgsBase = list(filter(lambda m: m.author == user, channelMsgsList))
	channelMsgs = len(channelMsgsBase)

	generalBotPrefixes = ['$', '$$', '?', '!', '*', '.', '`', '!!', '??']
	nonBotMsgs = len(list(filter(lambda m: m.author.bot != True, channelMsgsList)))
	botMsgs = len(list(filter(lambda m: m.author.bot == True, channelMsgsList)))

	nonCommandMsgsBase = list(filter(lambda m: any(m.content.startswith(prefix) for prefix in generalBotPrefixes) != True, channelMsgsBase))
	commandMsgsBase = list(filter(lambda m: any(m.content.startswith(prefix) for prefix in generalBotPrefixes), channelMsgsBase))
	nonCommandMsgs = len(nonCommandMsgsBase)
	commandMsgs = len(commandMsgsBase)

	tnonCommandMsgsBase = list(filter(lambda m: any(m.content.startswith(prefix) for prefix in generalBotPrefixes) != True, channelMsgsList))
	tcommandMsgsBase = list(filter(lambda m: any(m.content.startswith(prefix) for prefix in generalBotPrefixes), channelMsgsList))
	tnonCommandMsgs = len(tnonCommandMsgsBase)
	tcommandMsgs = len(tcommandMsgsBase)

	embed = discord.Embed(
		title=f'💬 Message Statistics: `{user.display_name}`',
		colour=discord.Colour.dark_purple(),
		timestamp=m.created_at,
		description=f'__**FROM `{user.display_name}`:**__\n‎\t**TOTAL MESSAGES**: `{format(channelMsgs)}`\n‎\t**NCM**: `{nonCommandMsgs}`\n‎\t**CM**: `{format(commandMsgs)}`\n__**IN {cast(discord.TextChannel, ctx.channel).mention}**__:\n‎\t**TOTAL MESSAGES**: `{format(len(channelMsgsList))}`\n‎\t**NON-BOT MESSAGES**: `{format(nonBotMsgs)}`\n‎\t**BOT MESSAGES**: `{format(botMsgs)}`\n‎\t**NCM**: `{format(tnonCommandMsgs)}`\n‎\t**CM**: `{format(tcommandMsgs)}`'
	).set_thumbnail(
		url=user.display_avatar.url
	).set_footer(text=f'NCM (Non-Command Messages) refers to messages that DO NOT start with: {", ".join(generalBotPrefixes)}; while CM (Command Messages) refers to those that do.')

	await m.edit(content=None, embed=embed)