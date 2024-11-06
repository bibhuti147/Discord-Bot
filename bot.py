# Import discord library
import asyncio
from collections import defaultdict
import discord
import os
import get_anime
import get_manga

# Create a client instance for the bot
intents = discord.Intents.default()  # Initialize default intents
intents.message_content = True  # Allows the bot to read message content
client = discord.Client(intents=intents)

# Track users who recently received anime info to respond to "thank you"
recent_requests = defaultdict(lambda: None)  # Stores last user and clears after a timeout


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
        embed = discord.Embed(color=discord.Color.orange())
        embed.set_image(url=image_url)
        await message.channel.send(embed=embed)

    if "love" in message.content.lower() and "mika" in message.content.lower():
        await message.channel.send(f"love you too {message.author}")

    if message.content.lower().startswith("mika") or message.content.lower().startswith("mika-chan") and message.content.lower().endswith("anime")  or message.content.lower().endswith("manga"):
        recent_requests[message.author.id] = None
        words = message.content.split() 
        name=" ".join(words[1:-1])
        if message.content.lower().endswith("anime"):
            await get_anime.searched_anime(message.channel,name)
        elif message.content.lower().endswith("manga"):
            await get_manga.searched_manga(message.channel,name)
        
        recent_requests[message.author.id] = True 
        await asyncio.sleep(60)
        recent_requests[message.author.id] = None

     # Respond to "thank you" if user recently searched for anime
    if message.content.lower() == "thank you" and recent_requests[message.author.id]:
        thankyou_imageurl = "https://i.imgur.com/wcjJjfC.jpeg"
        thankyou_embed = discord.Embed( 
            description="~Your Welcome~",
            color=discord.Color.pink()
        )
        thankyou_embed.set_image(url=thankyou_imageurl)
        await message.channel.send(embed=thankyou_embed) 
        recent_requests[message.author.id] = None  # Reset after responding
    
    
# Run the bot with the extracted token
client.run(os.getenv("DISCORD_TOKEN"))
