def random_error():
	'''
	Generates a random error message.
	'''
	import random
	messages = [
		'Oops...',
		'Uh-oh...',
		'Something isn\'t right...',
		'We\'ve hit a bump...',
		'Not so fast...',
		'Eek...' 
	]

	emojis = ['❌', '😲', '😱', '😶', '😵', '😮', '⚠']

	rand_message = random.choice(messages)
	rand_emoji = random.choice(emojis)
	return f'{rand_emoji} {rand_message}'

def get_config_key(s: str):
	'''
		Get a configuration's key value.

		Configuration fetching will generally resorts to a `settings.py` file at root.
		~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		If the file or the key is not found, it will resort to environmental variables (.env).
		~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		
	'''

	def import_path(path):
		import sys, os, importlib.util, importlib.machinery, importlib
		module_name = os.path.basename(path).replace('-', '_')
		spec = importlib.util.spec_from_loader(
	        module_name,
	        importlib.machinery.SourceFileLoader(module_name, path)
		)
		module = importlib.util.module_from_spec(spec) # type: ignore
		spec.loader.exec_module(module) # type: ignore
		sys.modules[module_name] = module
		return module

	import os
	ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	SETTINGS_PATH = os.path.join(ROOT_DIR, 'settings.py')
	if os.path.isfile(SETTINGS_PATH):
		variables = vars(import_path(SETTINGS_PATH))
		if variables.get(s) is None:
			from dotenv import load_dotenv
			load_dotenv()
			return os.environ.get(s)
		else:
			return variables.get(s)