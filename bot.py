# Disable __pycache__ generation
import sys
sys.dont_write_bytecode = True

# Safety check to make sure Python 3.8 or above is the runner of this code
if not sys.version or sys.version[:3] < '3.8':
	try:
		import termcolor # type: ignore
		import os
		os.system('color')
		print(termcolor.colored('ERROR:', 'red'), termcolor.colored('Unibot requires a version of >=3.8 of Python as it uses discord.py 2.0 which requires that Python version.', 'white'))
	except ModuleNotFoundError:
		print('ERROR:', 'Unibot requires a version of >=3.8 of Python as it uses discord.py 2.0 which requires that Python version.')
	exit()

# List of required environmental variables to check against
req_variables = [
	'TOKEN',
	# -- Chatbot API -- #
	'CHATBOT_BRAIN_ID',
	'CHATBOT_API_KEY',
	# -- Endpoints -- #
	'CHATBOT_API_ENDPOINT',
	'TRIVIA_API_ENDPOINT',
	'FACTS_API_ENDPOINT',
	'JOKES_API_ENDPOINT',
	'CATS_API_ENDPOINT',
	'DOGS_API_ENDPOINT',
	'FOXES_API_ENDPOINT',
	'DICTIONARY_API_ENDPOINT',
	# -- Google Search Engine -- #
	'GOOGLE_SEARCH_CX',
	'GOOGLE_SEARCH_API_KEY'
]

req_packages = [
	'python-dotenv',
	'discord.py[speed]'
]

from typing import Callable, List, Union, Tuple, Any
from types import FunctionType
from datetime import datetime

# Check if required packages are installed
try:
	import pkg_resources
	found_pkgs = {}
	for package in req_packages:
		try:
			dist = pkg_resources.get_distribution(package)
			if dist.key and dist.version:
				found_pkgs[dist.key] = True
			else:
				found_pkgs[dist.key] = False
		except pkg_resources.DistributionNotFound:
			found_pkgs[package] = False

	if any(found_pkgs[found_package] == False for found_package in found_pkgs):
		not_found_pkgs = []
		for found_package in found_pkgs:
			if found_pkgs[found_package] == False:
				not_found_pkgs.append(found_package)

		if len(not_found_pkgs) > 0:
			try:
				import termcolor # type: ignore
				import os
				os.system('color')

				print(termcolor.colored('ERROR:', 'red'), termcolor.colored(f'The following required packages are missing: {", ".join(not_found_pkgs)}', 'white'))
			except ModuleNotFoundError:
				print('ERROR:', f'The following required packages are missing: {", ".join(not_found_pkgs)}')

			exit()

except ModuleNotFoundError:
	try:
		import termcolor # type: ignore
		import os
		os.system('color')

		print(termcolor.colored('ERROR:', 'red'), termcolor.colored('Unibot requires the Python built-in "pkg_resources" module.', 'white'))
	except ModuleNotFoundError:
		print('ERROR:', 'Unibot requires the Python built-in "pkg_resources" module.')

	exit()

from discord.ext import commands
import discord, glob, os, importlib, inspect

# Check if code is run as module (py -3 bot.py) or script (py -3 -m bot)
try:
	# Disable __pycache__ generation
	import sys
	sys.dont_write_bytecode = True
	# When code is run as a module (py -3 bot.py), the __package__ key is None
	# Whilst if code is run as a script (py -3 -m bot), the __package__ key is equal to ''
	mod_name = vars(sys.modules[__name__])['__package__']
	if mod_name != '':
		try:
			import termcolor # type: ignore
			import os
			os.system('color')

			print(termcolor.colored('ERROR:', 'red'), termcolor.colored('You are running Unibot as a module, which will prevent the loading of local libraries. Please run as a script, as:\n\tpy -3 -m bot\n\t(or) python -m bot', 'white'))
		except ModuleNotFoundError:
			print('ERROR:', 'You are running Unibot as a module, which will prevent the loading of local libraries. Please run as a script, as:\n\tpy -3 -m bot\n\t(or) python -m bot')
		
		exit()

except ModuleNotFoundError:
	print('ERROR:', 'Unibot requires the Python built-in "sys" module.')
	exit()


# Get required variables
try:
	# Import settings.py/env fetching utility
	from lib.utils import get_config_key
	found_vars = []
	for req_var in req_variables:
		found_vars.append(get_config_key(req_var))

	# If there's any found variable that is None, check variables that are none and list them
	if any(fv is None for fv in found_vars):
		not_found_vars = []
		for i, fv in enumerate(found_vars):
			if fv is None:
				not_found_vars.append(req_variables[i])
		try:
			import termcolor # type: ignore
			import os
			os.system('color')

			print(termcolor.colored('ERROR:', 'red'), termcolor.colored(f'The following required configuration keys are missing: {", ".join(not_found_vars)}', 'white'))
		except ModuleNotFoundError:
			print('ERROR:', f'The following required configuration keys are missing: {", ".join(not_found_vars)}')
		
		exit()
except ModuleNotFoundError:
	try:
		import termcolor # type: ignore
		import os
		os.system('color')

		print(termcolor.colored('ERROR:', 'red'), termcolor.colored('Unibot requires the local "lib.utils" module.', 'white'))
	except ModuleNotFoundError:
		print('ERROR:', 'Unibot requires the local "lib.utils" module.')

	exit()

# Enable privileged Discord intents
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
		# Commands handler
		for file in glob.glob('./commands/**/*.py'):
			if file.endswith('.py'):
				dirname = os.path.basename(os.path.dirname(file))
				filename = os.path.basename(file).split('.')[0]
				# If not command is an unpublished/testing event
				if not filename.startswith('_'):
					time = datetime.now().strftime('%I:%M:%S %p')
					cmds = list(inspect.getmembers(importlib.import_module(f'commands.{dirname}.{filename}'), predicate=isCommand))
					# Check if command is a subcommand parent (group)
					if len(cmds) > 1 or any(isGroup(cmd) for cmd in cmds):
						main = filterGroup(cmds)
						# If there is no group command, continue searching
						if main is None:
							continue
						# Add group command
						self.add_command(main)
					else:
						# Add normal command
						self.add_command(cmds[0][1])
					print(f'{time} || Loaded command {filename}')
				else:
					continue

		# Events handler
		for file in os.listdir('./events'):
			if file.endswith('.py'):
				evname = os.path.basename(file).split('.')[0]
				# If not event is an unpublished/testing event
				if not evname.startswith('_'):
					time = datetime.now().strftime('%I:%M:%S %p')
					listn = filterFunction(list(inspect.getmembers(importlib.import_module(f'events.{evname}'), predicate=isCallable)))
					# If there is no event function/listener, continue searching
					if listn is None:
						continue
					# Add event listener
					self.add_listener(listn)
					print(f'{time} || Loaded event {evname}')
				else:
					continue

client = CustomBot(command_prefix=get_config_key('PREFIX') or '$$', help_command = None, intents=intents, heartbeat_timeout=60000)
client.run(format(get_config_key('TOKEN')))