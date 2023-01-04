import requests, json, discord, os

from discord.ext import commands
from typing import Union

from dotenv import load_dotenv

load_dotenv()


#Function that get the weather of any city using open weather api
def get_weather(city: str) -> Union[dict, str]:
    # Get your api key at "https://openweathermap.org/current"
    api_key = format(os.environ.get("WEATHER_API_KEY"))
    base_url = format(os.environ.get("WEATHER_API_ENDPOINT"))
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception if the request failed
        return response.json()
    except requests.RequestException as e:
        # Parse the error message as a JSON object and extract the "message" field
        error_message =json.loads(response.text)["message"]
        return {"message": error_message}



@commands.command()
async def weather(ctx: commands.Context, * city: str):
    # Join the city tuple into a single string
    city_name = " ".join(city)

    # Get the weather data for the specified city
    data = get_weather(city_name)

    # Check if the response is a string (error message)
    if isinstance(data, str):
        # Create an embed with the error message
        embed = discord.Embed(
            colour=discord.Colour.dark_red(),
            title="Error",
            description=data,
        )
        await ctx.send(embed=embed)
        return

    # Extract the error message if it exists
    if "message" in data:
        error_message = data["message"]
        # Create an embed with the error message
        embed = discord.Embed(
            colour=discord.Colour.dark_red(),
            title="Error",
            description=error_message,
        )
        await ctx.send(embed=embed)
        return

    # Check if the "name" field exists in the data
    if "name" not in data:
        # Create an embed with an error message
        embed = discord.Embed(
            colour=discord.Colour.dark_red(),
            title="Error",
            description="Failed to retrieve weather data. Please try again later.",
        )
        await ctx.send(embed=embed)
        return

    # Extract the temperature, humidity, and wind speed from the data
    name = data["name"]
    celsius = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    wind_speed_kph = data["wind"]["speed"]
    wind_direction = data["wind"]["deg"]

    # Converts Degrres value to north, south, east or west
    def degree_to_cardinal(degree):
        directions = ["North", "Northeast", "East", "Southeast", "South", "Southwest", "West", "Northwest"]
        index = int((degree + 22.5) / 45)
        return directions[index % 8]

    wind_direction_word = degree_to_cardinal(wind_direction)

    # Get the state of the weather
    weather_state = data["weather"][0]["description"]
    
    # Round the temperature and wind speed to two decimal places
    temperature = f"{celsius:.2f}"

    # Create an embed with the weather data
    embed = discord.Embed(
        colour=discord.Colour.dark_blue(),
        title=f"Weather Info in {name}",
        description=f"**Weather:** {weather_state.capitalize()}\n**Temperature:** {temperature}°C\n**Humidity:** {humidity}%\n**Wind Speed:** {wind_speed_kph:.2f}km/h to {wind_direction_word}"
    )

    # Send the embed message to the channel
    await ctx.send(embed=embed)




'''
Command made by Arktic 
Date: 4 Jan 2023

Descrption of code:

This is a Discord bot command that retrieves and displays weather information for 
a given city. When the command is invoked with a city name as an argument, it uses 
the OpenWeatherMap API to retrieve the current weather data for that city. It then 
displays the temperature, humidity, wind speed and direction, and a description of 
the current weather state in an embed message. If there is an error making the request 
or parsing the response, the command displays an error message in the embed message instead. 
This command can be useful for quickly getting weather information for a specific city without 
leaving Discord.
'''
