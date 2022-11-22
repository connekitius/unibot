def random_error():
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