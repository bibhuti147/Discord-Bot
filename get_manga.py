import aiohttp
import discord

# Define an asynchronous function to fetch the manga data
async def searched_manga(ctx,manga: str):
    try:
        if manga == "":
            return
        # Create an asynchronous HTTP session
        async with aiohttp.ClientSession() as session:
            # Send an asynchronous GET request
            async with session.get(f'https://api.jikan.moe/v4/manga?q={manga}') as response:
                # Check if the response is successful
                if response.status == 200:
                    data = await response.json()  # Convert the response to JSON
                    
                    # Extract and print the manga information
                    if data['data']:
                        manga_data = data['data'][0]
                        
                        manga_title = manga_data['titles'][0]['title']
                        manga_synopsis = manga_data['synopsis']
                        manga_url = manga_data['url']
                        manga_image = manga_data['images']['jpg']['image_url']

                        # Create an embed message with manga details
                        embed = discord.Embed(
                            title=manga_title,
                            url=manga_url,
                            description=manga_synopsis,
                            color=discord.Color.blue()
                        )
                        embed.set_thumbnail(url=manga_image)  # Set the manga image as the thumbnail

                        # Send the embed to the channel
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send("No results found for this manga.")
                else:
                    await ctx.send(f"Failed to retrieve data: {response.status}")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}") 
