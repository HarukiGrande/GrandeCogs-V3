import discord
from redbot.core import commands
import aiohttp

BaseCog = getattr(commands, "Cog", object)

class NexusHub(BaseCog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)

    @commands.group()
    @commands.guild_only()
    async def nexushub(self, ctx):
        """https://nexushub.co/"""
        pass

    @nexushub.command()
    async def item(self, ctx, *, item):
        """Item Lookup"""
        item = item.replace(" ", "-").replace("'", "")
        em = await self.itemlookup(item)
        await ctx.send(embed=em)

    #@commands.Cog.listener()
    #async def on_message(self, message):
        #print(dir(message))

    async def itemlookup(self, item):
        data = await (await self.session.get(f"https://api.nexushub.co/wow-classic/v1/item/{item}")).json()
        if "error" in data:
            em = discord.Embed(title=(data["reason"]).title(), color=0xff0000)
            em.set_footer(text="https://nexushub.co/")
            return em
        tooltip_data = data["tooltip"]
        em = discord.Embed(title=data["name"], url=f"https://classic.wowhead.com/item={data['itemId']}", colour=color=0xff0000)
        em.set_thumbnail(url=data["icon"])

        for label in tooltip_data:
            em.add_field(name=None, value=label["label"], inline=False)

        em.set_footer(text="https://nexushub.co/")

        return em
