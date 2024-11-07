import aiohttp
import discord
import math

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

genres = [{'name': 'action', 'id': 1}, {'name': 'adventure', 'id': 2}, {'name': 'avant garde', 'id': 5}, {'name': 'award winning', 'id': 46}, {'name': 'boys love', 'id': 28}, 
{'name': 'comedy', 'id': 4}, {'name': 'drama', 'id': 8}, {'name': 'fantasy', 'id': 10}, {'name': 'girls love', 'id': 26}, {'name': 'gourmet', 'id': 47}, {'name': 'horror', 'id': 14}, {'name': 'mystery', 'id': 7}, {'name': 'romance', 'id': 22}, {'name': 'sci-fi', 'id': 24}, {'name': 'slice of life', 'id': 36}, {'name': 'sports', 'id': 30}, {'name': 'supernatural', 'id': 37}, {'name': 'suspense', 'id': 41}, {'name': 'ecchi', 'id': 9}, {'name': 'erotica', 'id': 49}, {'name': 'hentai', 'id': 12}, 
{'name': 'adult cast', 'id': 50}, {'name': 'anthropomorphic', 'id': 51}, {'name': 'cgdct', 'id': 52}, {'name': 'childcare', 'id': 53}, {'name': 'combat sports', 'id': 54}, {'name': 'crossdressing', 'id': 81}, {'name': 'delinquents', 'id': 55}, {'name': 'detective', 'id': 39}, {'name': 'educational', 'id': 56}, {'name': 'gag humor', 'id': 57}, {'name': 'gore', 'id': 58}, {'name': 'harem', 'id': 35}, {'name': 'high stakes game', 'id': 59}, {'name': 'historical', 'id': 13}, {'name': 'idols (female)', 'id': 60}, {'name': 'idols (male)', 'id': 61}, {'name': 'isekai', 'id': 62}, {'name': 'iyashikei', 'id': 63}, {'name': 'love polygon', 'id': 64}, {'name': 'magical sex shift', 'id': 65}, {'name': 'mahou shoujo', 'id': 66}, {'name': 'martial arts', 'id': 17}, {'name': 'mecha', 'id': 18}, {'name': 'medical', 'id': 67}, {'name': 'military', 'id': 38}, {'name': 'music', 'id': 19}, {'name': 'mythology', 'id': 6}, {'name': 'organized crime', 'id': 68}, {'name': 'otaku culture', 'id': 69}, {'name': 'parody', 'id': 20}, {'name': 'performing arts', 'id': 70}, {'name': 'pets', 'id': 71}, {'name': 'psychological', 'id': 40}, {'name': 'racing', 'id': 3}, {'name': 'reincarnation', 'id': 72}, {'name': 'reverse harem', 'id': 73}, {'name': 'love status quo', 'id': 74}, {'name': 'samurai', 'id': 21}, {'name': 'school', 'id': 23}, 
{'name': 'showbiz', 'id': 75}, {'name': 'space', 'id': 29}, {'name': 'strategy game', 'id': 11}, {'name': 'super power', 'id': 31}, {'name': 'survival', 'id': 76}, {'name': 'team sports', 'id': 77}, {'name': 'time travel', 'id': 78}, {'name': 'vampire', 'id': 32}, {'name': 'video game', 'id': 79}, {'name': 'visual arts', 'id': 80}, {'name': 'workplace', 'id': 48}, {'name': 'urban fantasy', 'id': 82}, {'name': 'villainess', 'id': 83}, {'name': 'josei', 'id': 43}, {'name': 'kids', 'id': 15}, {'name': 'seinen', 'id': 42}, {'name': 'shoujo', 'id': 25}, {'name': 'shounen', 'id': 27}]

async def top_anime(ctx,param: str,sid: int,eid: int):
    url = ""
    page = 1 + math.floor(sid/25)
    sid = sid - 25*(page-1)
    eid = eid - 25*(page-1)
    try:
        if param == "10":
            url = f'https://api.jikan.moe/v4/top/anime?page={page}'
        elif param == "recent" or param == "current":
            url = f"https://api.jikan.moe/v4/top/anime?page={page}&filter=airing"
        elif param == "upcoming":
            url = f"https://api.jikan.moe/v4/top/anime?page={page}&filter=upcoming"
        else:
            genre = next((genre for genre in genres if genre["name"] == param.lower()), None)
            if(genre):
                url = f"https://api.jikan.moe/v4/anime?page={page}&genres={genre['id']}&order_by=score&sort=desc"
            else:
                return await ctx.send("No results found for this genre.") 

        async with aiohttp.ClientSession() as session: 
            # Send an asynchronous GET request
            async with session.get(url) as response:
                # Check if the response is successful
                if response.status == 200:
                    data = await response.json()  # Convert the response to JSON
                    
                    # Extract and print the anime information
                    if data['data']:
                        topanime_data = data['data'][sid:eid]
                        for anime_data in topanime_data:
                            anime_title = anime_data['title']
                            anime_excerpt = anime_data['title_english']
                            anime_url = anime_data['url']
                            anime_image = anime_data['images']['jpg']['image_url'] 
                            # Create an embed message with anime details
                            embed = discord.Embed(
                                title=anime_title,
                                url=anime_url,
                                description=anime_excerpt,
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