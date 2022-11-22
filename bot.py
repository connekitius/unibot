import sys
sys.dont_write_bytecode = True

from typing import Callable, List, Union, Tuple, Any
from types import FunctionType
from datetime import datetime
from dotenv import load_dotenv
from discord.ext import commands
import discord, glob, os, importlib, inspect, settings
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

isCallable: Callable[[Any], bool] = lambda v: isinstance(v, Callable)
isCommand: Callable[[Any], bool] = lambda v: isinstance(v, commands.core.Command)
isGroup: Callable[[Any], bool] = lambda v: isinstance(v, commands.core.Group)
isFunction: Callable[[Any], bool] = lambda v: isinstance(v, FunctionType)
filterFunction: Callable[[Union[List, Tuple]], Union[FunctionType, None]] = lambda v: list(filter(isFunction, list(map(lambda x: x[1] or None, list(v)))))[0] or None
filterGroup: Callable[[Union[List, Tuple]], Union[commands.core.Group, None]] = lambda v: list(filter(isGroup, list(map(lambda x: x[1] or None, list(v)))))[0] or None

class CustomBot(commands.Bot):
	async def setup_hook(self):
		for file in glob.glob('./commands/**/*.py'):
			if file.endswith('.py'):
				dirname = os.path.basename(os.path.dirname(file))
				filename = os.path.basename(file).split('.')[0]
				if not filename.startswith('_'):
					time = datetime.now().strftime('%I:%M:%S %p')
					cmds = list(inspect.getmembers(importlib.import_module(f'commands.{dirname}.{filename}'), predicate=isCommand))
					if len(cmds) > 1 or any(isGroup(cmd) for cmd in cmds):
						main = filterGroup(cmds)
						if main is None:
							continue
						self.add_command(main)
					else:
						self.add_command(cmds[0][1])
					print(f'{time} || Loaded command {filename}')
				else:
					continue

		for file in os.listdir('./events'):
			if file.endswith('.py'):
				evname = os.path.basename(file).split('.')[0]
				if not evname.startswith('_'):
					time = datetime.now().strftime('%I:%M:%S %p')
					listn = filterFunction(list(inspect.getmembers(importlib.import_module(f'events.{evname}'), predicate=isCallable)))
					if listn is None:
						continue
					self.add_listener(listn)
					print(f'{time} || Loaded event {evname}')
				else:
					continue

client = CustomBot(command_prefix=settings.PREFIX or '$$', help_command = None, intents=intents, heartbeat_timeout=60000)
client.run(format(settings.TOKEN or os.environ.get('TOKEN')))