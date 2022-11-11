import sys
sys.dont_write_bytecode = True

from typing import Callable, List
from colorama import init, Fore
from ast import ClassDef
from datetime import datetime
from dotenv import load_dotenv
from discord.ext import commands
import discord, glob, os, importlib, inspect

import settings

init()
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

def isCallable(v):
	return isinstance(v, Callable)

def isCommand(v):
	return isinstance(v, commands.core.Command)

def isCog(v):
	return isinstance(v, commands.cog.CogMeta)

def getCommandClassName(v):
	return v.__name__

def hasClassWithName(l: List, n: str):
	res = []
	for v in l:
		if isinstance(v, ClassDef) and getCommandClassName(v).lower() == n.lower():
			res.append(True)
		else:
			res.append(False)

	if any(res) == True:
		return True
	else:
		return False

#testing git, idk how this works!!
class CustomBot(commands.Bot):
	async def setup_hook(self):
		for file in glob.glob('./commands/**/*.py'):
			if file.endswith('.py'):
				dirname = os.path.basename(os.path.dirname(file))
				filename = os.path.basename(file).split('.')[0]
				time = datetime.now().strftime('%I:%M:%S %p')
				print(Fore.BLUE + f'{time} ' + Fore.YELLOW + '[LOADING	] ' + Fore.LIGHTBLACK_EX + f'Loading command {filename}...', end='\r')
				file = inspect.getmembers(importlib.import_module(f'commands.{dirname}.{filename}'), predicate=isCommand)
				self.add_command(file[0][1])
				print(Fore.BLUE + f'{time} ' + Fore.GREEN + '[SUCCESS	] ' + Fore.LIGHTBLACK_EX + f'Loaded command {filename}		')

		for file in os.listdir('./bot_events'):
			if file.endswith('.py'):
				evname = os.path.basename(file).split('.')[0]
				time = datetime.now().strftime('%I:%M:%S %p')
				print(Fore.BLUE + f'{time} ' + Fore.YELLOW + '[LOADING	] ' + Fore.LIGHTBLACK_EX + f'Loading event {evname}...', end='\r')
				listn: Callable = inspect.getmembers(importlib.import_module(f'bot_events.{evname}'), predicate=isCallable)[0][1]
				self.add_listener(listn)
				print(Fore.BLUE + f'{time} ' + Fore.GREEN + '[SUCCESS	] ' + Fore.LIGHTBLACK_EX + f'Loaded event {evname}		')

client = CustomBot(command_prefix=(settings.PREFIX), help_command = None, intents=intents, heartbeat_timeout=60000)
client.run(settings.TOKEN)
#FUCK YOU AMIN AM USING MY OWN WAY
