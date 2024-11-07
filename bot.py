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
topanime_requests = defaultdict(lambda: None)


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

    if message.content.lower().startswith("mika find") and message.content.lower().endswith("anime") or message.content.lower().endswith("manga"):
        recent_requests[message.author.id] = None
        words = message.content.split() 
        name=" ".join(words[2:-1])
        if words[-1].lower() == "anime":
            await get_anime.searched_anime(message.channel,name,0)
            recent_requests[message.author.id]={'type':'anime','name':name,'id':0}
        elif words[-1].lower() == "manga":
            await get_manga.searched_manga(message.channel,name,0)
            recent_requests[message.author.id]={'type':'manga','name':name,'id':0}
         
        await asyncio.sleep(180)
        recent_requests[message.author.id] = None

     # Respond to "thank you" if user recently searched for anime
    if message.author.id in recent_requests and recent_requests[message.author.id]:
        if message.content.lower() == "thank you":
            recent_requests[message.author.id] = None  # Reset after responding
            thankyou_imageurl = "https://i.imgur.com/wcjJjfC.jpeg"
            thankyou_embed = discord.Embed( 
                description="~Your Welcome~",
                color=discord.Color.pink()
            )
            thankyou_embed.set_image(url=thankyou_imageurl)
            await message.channel.send(embed=thankyou_embed) 
        
        elif message.content.lower() == "not this one":
             # Retrieve the last search details from `recent_requests`
            last_search = recent_requests[message.author.id]
            last_search['id']+=1
            if last_search['type'] == 'anime':
                await get_anime.searched_anime(message.channel, last_search['name'],last_search['id'])
            elif last_search['type'] == 'manga':
                await get_manga.searched_manga(message.channel, last_search['name'],last_search['id'])
            await asyncio.sleep(60)
            recent_requests[message.author.id] = None  # Reset after responding
         

    if message.content.lower().startswith("mika give me top 10") and message.content.lower().endswith("anime"):
        topanime_requests[message.author.id] = None
        twords=message.content.split()
        tname=" ".join(twords[-2:-1]) 
        await get_anime.top_anime(message.channel,tname,0,10)
        topanime_requests[message.author.id] = {"name":words[-2],"sid":0,"eid":10}
        await asyncio.sleep(180)
        topanime_requests[message.author.id] = None

    if message.author.id in topanime_requests and topanime_requests[message.author.id]:
        if message.content.lower() == "give me some more":
            top_search = topanime_requests[message.author.id]
            top_search['sid'] = top_search["eid"]
            top_search['eid'] += 5
            await get_anime.top_anime(message.channel,top_search['name'],top_search['sid'],top_search['eid'])
            await asyncio.sleep(60)
            
        elif message.content.lower() == "thank you":
            topanime_requests[message.author.id] = None
            thankyou_imageurl = "https://i.imgur.com/wcjJjfC.jpeg"
            thankyou_embed = discord.Embed( 
                description="~Your Welcome~",
                color=discord.Color.pink()
            )
            thankyou_embed.set_image(url=thankyou_imageurl)
            await message.channel.send(embed=thankyou_embed)

    
# Run the bot with the extracted token
client.run(os.getenv("DISCORD_TOKEN"))
