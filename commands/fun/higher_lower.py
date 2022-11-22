import random, discord
from typing import Union
from discord.ext import commands

class HigherLower(discord.ui.View):
	def __init__(self, base: int, guess: int, author: Union[discord.User, discord.Member]):
		super().__init__()
		self.baseNum = base
		self.guess = guess
		self.author= author

	@discord.ui.button(label='HIGHER', emoji='⬆')
	async def higherlower_higher(self, interaction: discord.Interaction, button: discord.ui.Button):
		if not interaction.message or not interaction.message.embeds or not interaction.message.embeds[0]:
				return;

		if self.baseNum < self.guess:
			embed = interaction.message.embeds[0]
			embed.title = '↕ Higher or Lower? `(✅)`'
			embed.description = f'*You won! My number was:*\n‎\t**{self.guess}**'
			return await interaction.response.edit_message(embed=embed, view=None)
		else:
			embed = interaction.message.embeds[0]
			embed.title = '↕ Higher or Lower? `(❌)`'
			embed.description = f'*You lost... My number was:*\n‎\t**{self.guess}**'
			return await interaction.response.edit_message(embed=embed, view=None)

	@discord.ui.button(label='LOWER', emoji='⬇')
	async def higherlower_lower(self, interaction: discord.Interaction, button: discord.ui.Button):
		if not interaction.message or not interaction.message.embeds or not interaction.message.embeds[0]:
				return;

		if self.baseNum > self.guess:
			embed = interaction.message.embeds[0]
			embed.title = '↕ Higher or Lower? `(✅)`'
			embed.description = f'*You won! My number was:*\n‎\t**{self.guess}**'
			return await interaction.response.edit_message(embed=embed, view=None)
		else:
			embed = interaction.message.embeds[0]
			embed.title = '↕ Higher or Lower? `(❌)`'
			embed.description = f'*You lost... My number was:*\n‎\t**{self.guess}**'
			return await interaction.response.edit_message(embed=embed, view=None)

	async def interaction_check(self, interaction: discord.Interaction) -> bool:
		return interaction.user == self.author

@commands.command(aliases=["hl"], extras={
	"examples": "$$hl"
})
@commands.cooldown(1, 5, commands.BucketType.user)
async def higher_lower(ctx: commands.Context):
	baseNum = random.randint(1, 100)
	guess = random.randint(1, 100)
		
	while baseNum == guess:
		baseNum = random.randint(1, 100)
		guess = random.randint(1, 100)

	embed = discord.Embed(
		title='↕ Higher or Lower? `(❔)`',
		description=f'*Is my number\n‎\t**HIGHER OR LOWER**\nthan {baseNum}?*',
		colour=discord.Colour.dark_blue()
	)

	await ctx.reply(embed=embed, view=HigherLower(base=baseNum, guess=guess, author=ctx.author))