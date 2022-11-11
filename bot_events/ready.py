from colorama import Fore

Blue = Fore.BLUE
Green = Fore.GREEN

async def on_ready():
	print(Green+ "Logged in!")
	print(Blue+ "Username: ", Red+ f"{client.user.name}")
    	print(Blue+ "id:", Red+ f"{client.user.id}")
    	print("")
