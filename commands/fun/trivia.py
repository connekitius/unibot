import random
from typing import List, Literal, Optional, TypedDict
import requests, discord, os
from discord.ext import commands

difficultyQueries = {
	'easy': 'difficulty=easy',
	'medium': 'difficulty=medium',
	'hard': 'difficulty=hard'
}

numbers = {
	0: '1️⃣',
	1: '2️⃣',
	2: '3️⃣',
	3: '4️⃣'
}

class TriviaQuestion(TypedDict):
	category: str
	id: str
	correctAnswer: str
	incorrectAnswers: List[str]
	question: str
	tags: List[str]
	type: str
	difficulty: Literal['easy', 'medium', 'hard']
	regions: List[str]

class TriviaChoices(discord.ui.View):
	def __init__(self, triviaChoices: List[str], question: str, rightChoice: str, timeout: Optional[float] = 180):
		self.triviaChoices = triviaChoices
		self.rightChoice = rightChoice
		self.question = question
		super().__init__(timeout=timeout)

	@discord.ui.button(emoji=numbers[0])
	async def trivia_choice_one(self, interaction: discord.Interaction, _button: discord.ui.Button): # ignore
		if not interaction.message or not interaction.message.embeds or not interaction.message.embeds[0]:
				return;

		if self.triviaChoices[0] == self.rightChoice:
			embed = interaction.message.embeds[0]
			embed.title = '✅ We\'ve got a winner!'
			embed.description = (embed.description or f'{numbers[0]} {self.rightChoice}').replace(self.rightChoice, f'**{self.rightChoice}**')
			embed.add_field(name='Question', value=self.question)
			return await interaction.response.edit_message(embed=embed, view=None)
		else:
			embed = interaction.message.embeds[0]
			embed.title = '❌ But not everybody\'s a winner...'
			embed.description = (embed.description or f'{numbers[0]} {self.rightChoice}').replace(self.rightChoice, f'**{self.rightChoice}**')
			embed.add_field(name='Question', value=self.question)
			return await interaction.response.edit_message(embed=embed, view=None)

	@discord.ui.button(emoji=numbers[1])
	async def trivia_choice_two(self, interaction: discord.Interaction, _button: discord.ui.Button):
		if not interaction.message or not interaction.message.embeds or not interaction.message.embeds[0]:
				return;

		if self.triviaChoices[1] == self.rightChoice:
			embed = interaction.message.embeds[0]
			embed.title = '✅ We\'ve got a winner!'
			embed.description = (embed.description or f'{numbers[1]} {self.rightChoice}').replace(self.rightChoice, f'**{self.rightChoice}**')
			embed.add_field(name='Question', value=self.question)
			return await interaction.response.edit_message(embed=embed, view=None)
		else:
			embed = interaction.message.embeds[0]
			embed.title = '❌ But not everybody\'s a winner...'
			embed.description = (embed.description or f'{numbers[1]} {self.rightChoice}').replace(self.rightChoice, f'**{self.rightChoice}**')
			embed.add_field(name='Question', value=self.question)
			return await interaction.response.edit_message(embed=embed, view=None)

	@discord.ui.button(emoji=numbers[2])
	async def trivia_choice_three(self, interaction: discord.Interaction, _button: discord.ui.Button):
		if not interaction.message or not interaction.message.embeds or not interaction.message.embeds[0]:
				return;

		if self.triviaChoices[2] == self.rightChoice:
			embed = interaction.message.embeds[0]
			embed.title = '✅ We\'ve got a winner!'
			embed.description = (embed.description or f'{numbers[2]} {self.rightChoice}').replace(self.rightChoice, f'**{self.rightChoice}**')
			embed.add_field(name='Question', value=self.question)
			return await interaction.response.edit_message(embed=embed, view=None)
		else:
			embed = interaction.message.embeds[0]
			embed.title = '❌ But not everybody\'s a winner...'
			embed.description = (embed.description or f'{numbers[2]} {self.rightChoice}').replace(self.rightChoice, f'**{self.rightChoice}**')
			embed.add_field(name='Question', value=self.question)
			return await interaction.response.edit_message(embed=embed, view=None)

	@discord.ui.button(emoji=numbers[3])
	async def trivia_choice_four(self, interaction: discord.Interaction, button: discord.ui.Button):
		if not interaction.message or not interaction.message.embeds or not interaction.message.embeds[0]:
				return;

		if self.triviaChoices[3] == self.rightChoice:
			embed = interaction.message.embeds[0]
			embed.title = '✅ We\'ve got a winner!'
			embed.description = (embed.description or f'{numbers[3]} {self.rightChoice}').replace(self.rightChoice, f'**{self.rightChoice}**')
			embed.add_field(name='Question', value=self.question)
			return await interaction.response.edit_message(embed=embed, view=None)
		else:
			embed = interaction.message.embeds[0]
			embed.title = '❌ But not everybody\'s a winner...'
			embed.description = (embed.description or f'{numbers[3]} {self.rightChoice}').replace(self.rightChoice, f'**{self.rightChoice}**')
			embed.add_field(name='Question', value=self.question)
			return await interaction.response.edit_message(embed=embed, view=None)

@commands.command()
@commands.cooldown(5, 20, commands.BucketType.user)
async def trivia(ctx: commands.Context, difficulty: Optional[str]):
	endpoint = format(os.environ.get('TRIVIA_API_ENDPOINT')) + '?limit=10'
	if difficulty and difficulty.lower() in ['easy', 'medium', 'hard']:
		endpoint += f'&{difficultyQueries[difficulty.lower()]}'

	res = requests.get(endpoint)
	if res.status_code == 200:
		trivList: List[TriviaQuestion] = res.json()
		if len(trivList) > 0:
			question = random.choice(trivList)
			choices: List[str] = []; choices.extend(question["incorrectAnswers"])
			choices.insert(random.randint(0, 3), question["correctAnswer"])

			mapped = list(map(lambda v: f'{format(numbers.get(choices.index(v)))} {v.strip(" ")}', choices))
			stripped = question["question"].strip(' ')

			embed = discord.Embed(
				colour=discord.Colour.dark_blue(),
				title=f'❓ Trivia: `{stripped}`',
				description='\n'.join(mapped)
			)

			if len(question["tags"]) > 0:
				embed.set_footer(text=f'Tags: {", ".join(question["tags"])}')
			elif len(question["regions"]) > 0:
				embed.set_footer(text=f'{embed.footer.text + " | " if embed.footer.text is not None else ""}Region{"s" if len(question["regions"]) > 1 else ""}: {", ".join(question["regions"])}')

			embed.add_field(
				name='Category',
				value=question["category"]
			).add_field(
				name='Difficulty',
				value = question["difficulty"].capitalize()
			)

			await ctx.reply(embed=embed, view=TriviaChoices(triviaChoices=choices, question=question["question"], rightChoice=question["correctAnswer"]))
	else:
		embed = discord.Embed(
			title='❌ Trivia Error: `FetchError`',
			colour=discord.Colour.dark_blue(),
			description=f'```Failed to fetch trivia with a status code of {res.status_code}```'
		)
		return await ctx.reply(embed=embed)