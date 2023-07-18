import asyncio
import aiohttp
import nextcord


async def search_manga(query: str, chapter: int = None):
    if chapter is None:
        chapter = 1
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://manga-apiv2.herokuapp.com/ms/?name={query}") as resp:
            data = await resp.json()
            print(data)
            url = data["results"][0]["url"]
            async with session.get(
                    f"https://manga-apiv2.herokuapp.com/get_chapter/?url={url}&chapter={chapter}") as img:
                data = await img.json()
                print(data)
                embed = nextcord.Embed(title=f"{data['name']}").set_image(url=data['pages'][10])
                return embed


async def get_panels(query: str, url: str, chapter: int) -> []:
    if chapter is None:
        chapter = 1
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://manga-apiv2.herokuapp.com/ms/?name={query}") as resp:
            data = await resp.json()
            print(data)
            url = data["results"][0]["url"]
            async with session.get(
                    f"https://manga-apiv2.herokuapp.com/get_chapter/?url={url}&chapter={chapter}") as img:
                data = await img.json()
    return data['pages']
