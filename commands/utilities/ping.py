import discord, time
from discord.ext import commands

@commands.command(description='Get bot latency.', extras={
	'examples': ['$$ping']
})
async def ping(ctx: commands.Context):
	bot: commands.Bot = ctx.bot
	embed = discord.Embed(
		title='🏓 Pong!',
		colour=discord.Colour.dark_purple(),
		description=f'__API Latency__:‎\t`{round(bot.latency * 1000, 1)}`ms\n__Message Latency__:‎\t`fetching...`\n__Editing Latency__:‎\t`fetching...`'
	)

	start = time.perf_counter()
	m = await ctx.reply(embed=embed)
	end = time.perf_counter()
	editStart = time.perf_counter()
	messageLatency = round((end - start) * 1000, 1)
	
	embed2 = discord.Embed(
		title='🏓 Pong!',
		colour=discord.Colour.dark_purple(),
		description=f'__API Latency__:‎\t`{round(bot.latency * 1000, 1)}`ms\n__Message Latency__:‎\t`{messageLatency}`ms\n__Editing Latency__:‎\t`fetching...`'
	)
	m = await m.edit(embed=embed2)
	editEnd = time.perf_counter()

	editLatency = round((editEnd - editStart) * 1000, 1)
	embed3 = discord.Embed(
		title='🏓 Pong!',
		colour=discord.Colour.dark_purple(),
		description=f'__API Latency__:‎\t`{round(bot.latency * 1000, 1)}`ms\n__Message Latency__:‎\t`{messageLatency}`ms\n__Editing Latency__:‎\t`{editLatency}`ms'
	)
	await m.edit(embed=embed3)