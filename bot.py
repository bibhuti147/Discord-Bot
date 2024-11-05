# Import discord library
import discord
import os
import get_anime

# Create a client instance for the bot
intents = discord.Intents.default()  # Initialize default intents
intents.message_content = True  # Allows the bot to read message content
client = discord.Client(intents=intents)

# Define an event that triggers when the bot has logged in
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# Define an event that triggers when a message is received
@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    # Respond to a specific message content
    if message.content.startswith('!hello'):
        await message.channel.send('Hello XD!')

     # Check if the message says "hello bot_name"
    if message.content.lower() == "hello mika":  # Replace "bot_name" with your bot's name
        # Define the URL of the image to be sent
        image_url = "https://i.imgur.com/kWUyjrO.png"
        
        # Send the image using embed
        embed = discord.Embed()
        embed.set_image(url=image_url)
        await message.channel.send(embed=embed)

    if "love" in message.content.lower() and "mika" in message.content.lower():
        await message.channel.send(f"love you too {message.author}")

    if message.content.lower().starstwith("anime") and message.content.lower().endstwith("mika"):
        words = message.content.split()

        anime_name=" ".join(words[1:-1])
        await get_anime.searched_anime(message.channel,anime_name)

# Run the bot with the extracted token
client.run(os.getenv("DISCORD_TOKEN"))
