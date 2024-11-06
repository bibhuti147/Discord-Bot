import aiohttp
import discord

# Define an asynchronous function to fetch the anime data
async def searched_anime(ctx,anime: str,id: int):
    try:
        if anime == "":
            return
        # Create an asynchronous HTTP session
        async with aiohttp.ClientSession() as session:
            # Send an asynchronous GET request
            async with session.get(f'https://api.jikan.moe/v4/anime?q={anime}') as response:
                # Check if the response is successful
                if response.status == 200:
                    data = await response.json()  # Convert the response to JSON
                    
                    # Extract and print the anime information
                    if data['data']:
                        anime_data = data['data'][id]
                        
                        anime_title = anime_data['title']
                        anime_synopsis = anime_data['synopsis']
                        anime_url = anime_data['url']
                        anime_image = anime_data['images']['jpg']['image_url']

                        # Create an embed message with anime details
                        embed = discord.Embed(
                            title=anime_title,
                            url=anime_url,
                            description=anime_synopsis,
                            color=discord.Color.blue()
                        )
                        embed.set_thumbnail(url=anime_image)  # Set the anime image as the thumbnail

                        # Send the embed to the channel
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send("No results found for this anime.")
                else:
                    await ctx.send(f"Failed to retrieve data: {response.status}")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}") 
