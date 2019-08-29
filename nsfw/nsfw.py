import discord
from redbot.core import commands
from bs4 import BeautifulSoup
import random
import aiohttp

BaseCog = getattr(commands, "Cog", object)

class NSFW(BaseCog):
    """NSFW commands."""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)

    @commands.group()
    @commands.guild_only()
    async def nsfw(self, ctx):
        """NSFW Commands"""
        pass

    @nsfw.command()
    @commands.is_nsfw()
    async def yandere(self, ctx):
        """Random Image From Yandere"""
        try:
            query = ("https://yande.re/post/random")
            page = await (await self.session.get(query)).text()
            soup = BeautifulSoup(page, 'html.parser')
            image = soup.find(id="highres").get("href")
            await ctx.send(image)
        except Exception as e:
            await ctx.send(f":x: **Error:** `{e}`")

    @nsfw.command()
    @commands.is_nsfw()
    async def konachan(self, ctx):
        """Random Image From Konachan"""
        try:
            query = ("https://konachan.com/post/random")
            page = await (await self.session.get(query)).text()
            soup = BeautifulSoup(page, 'html.parser')
            image = soup.find(id="highres").get("href")
            await ctx.send(image)
        except Exception as e:
            await ctx.send(f":x: **Error:** `{e}`")

    @nsfw.command()
    @commands.is_nsfw()
    async def e621(self, ctx):
        """Random Image From e621"""
        try:
            query = ("https://e621.net/post/random")
            page = await (await self.session.get(query)).text()
            soup = BeautifulSoup(page, 'html.parser')
            image = soup.find(id="highres").get("href")
            await ctx.send(image)
        except Exception as e:
            await ctx.send(f":x: **Error:** `{e}`")

    @nsfw.command()
    @commands.is_nsfw()
    async def rule34(self, ctx):
        """Random Image From rule34"""
        try:
            query = ("http://rule34.xxx/index.php?page=post&s=random")
            page = await (await self.session.get(query)).text()
            soup = BeautifulSoup(page, 'html.parser')
            image = soup.find(id="image").get("src")
            await ctx.send(image)
        except Exception as e:
            await ctx.send(f":x: **Error:** `{e}`")

    @nsfw.command()
    @commands.is_nsfw()
    async def danbooru(self, ctx):
        """Random Image From Danbooru"""
        try:
            query = ("http://danbooru.donmai.us/posts/random")
            page = await (await self.session.get(query)).text()
            soup = BeautifulSoup(page, 'html.parser')
            image = soup.find(id="image").get("src")
            await ctx.send(image)
        except Exception as e:
            await ctx.send(f":x: **Error:** `{e}`")

    @nsfw.command()
    @commands.is_nsfw()
    async def gelbooru(self, ctx):
        """Random Image From Gelbooru"""
        try:
            query = ("http://www.gelbooru.com/index.php?page=post&s=random")
            page = await (await self.session.get(query)).text()
            soup = BeautifulSoup(page, 'html.parser')
            image = soup.find(id="image").get("src")
            await ctx.send(image)
        except Exception as e:
            await ctx.send(f":x: **Error:** `{e}`")

    @nsfw.command()
    @commands.is_nsfw()
    async def tbib(self, ctx):
        """Random Image From TBIB"""
        try:
            query = ("http://www.tbib.org/index.php?page=post&s=random")
            page = await (await self.session.get(query)).text()
            soup = BeautifulSoup(page, 'html.parser')
            image = soup.find(id="image").get("src")
            await ctx.send("http:" + image)
        except Exception as e:
            await ctx.send(f":x: **Error:** `{e}`")

    @nsfw.command()
    @commands.is_nsfw()
    async def xbooru(self, ctx):
        """Random Image From Xbooru"""
        try:
            query = ("http://xbooru.com/index.php?page=post&s=random")
            page = await (await self.session.get(query)).text()
            soup = BeautifulSoup(page, 'html.parser')
            image = soup.find(id="image").get("src")
            await ctx.send(image)
        except Exception as e:
            await ctx.send(f":x: **Error:** `{e}`")

    @nsfw.command()
    @commands.is_nsfw()
    async def furrybooru(self, ctx):
        """Random Image From Furrybooru"""
        try:
            query = ("http://furry.booru.org/index.php?page=post&s=random")
            page = await (await self.session.get(query)).text()
            soup = BeautifulSoup(page, 'html.parser')
            image = soup.find(id="image").get("src")
            await ctx.send(image)
        except Exception as e:
            await ctx.send(f":x: **Error:** `{e}`")

    @nsfw.command()
    @commands.is_nsfw()
    async def drunkenpumken(self, ctx):
        """Random Image From DrunkenPumken"""
        try:
            query = ("http://drunkenpumken.booru.org/index.php?page=post&s=random")
            page = await (await self.session.get(query)).text()
            soup = BeautifulSoup(page, 'html.parser')
            image = soup.find(id="image").get("src")
            await ctx.send(image)
        except Exception as e:
            await ctx.send(f":x: **Error:** `{e}`")

    @nsfw.command()
    @commands.is_nsfw()
    async def astolfo(self, ctx):
        """Random Image From UnlimitedAstolfo"""
        try:
            query = ("http://unlimitedastolfo.works/random_image/view")
            page = await (await self.session.get(query)).text()
            soup = BeautifulSoup(page, 'html.parser')
            image = soup.find(id="main_image").get("href")
            await ctx.send(f"http://unlimitedastolfo.works/{image}")
        except Exception as e:
            await ctx.send(f":x: **Error:** `{e}`")

    #@nsfw.command()
    #@commands.guild_only()
    #@commands.is_nsfw()
    #async def lolibooru(self, ctx):
        #"""Random Image From Lolibooru"""
        #try:
            #query = ("https://lolibooru.moe/post/random/")
            #page = await (await self.session.get(query)).text()
            #soup = BeautifulSoup(page, 'html.parser')
            #image = soup.find(id="image").get("src")
            #image = image.replace(' ', '%20')
            #await ctx.send(image)
        #except Exception as e:
            #await ctx.send(f":x: **Error:** `{e}`")

    @nsfw.command()
    @commands.is_nsfw()
    async def ysearch(self, ctx, *tags: str):
        """Search Yandere With A Tag"""
        if tags == ():
            await ctx.send(":warning: Tags are missing.")
        else:
            try:
                tags = ("+").join(tags)
                query = ("https://yande.re/post.json?limit=42&tags=" + tags)
                json = await (await self.session.get(query)).json()
                if json != []:
                    await ctx.send(random.choice(json)['jpeg_url'])
                else:
                    await ctx.send(":warning: Yande.re has no images for requested tags.")
            except Exception as e:
                await ctx.send(f":x: **Error:** `{e}`")
