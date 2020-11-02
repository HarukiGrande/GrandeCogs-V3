import discord, aiohttp, re
from redbot.core import commands

BaseCog = getattr(commands, "Cog", object)

class NexusHub(BaseCog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)

    @commands.group()
    @commands.guild_only()
    async def nexushub(self, ctx):
        """www.nexushub.co"""
        pass

    @nexushub.command()
    async def item(self, ctx, *, item):
        """Item Lookup"""
        item = item.replace(" ", "-")
        data = await self.itemlookup(item)
        em = await self.embedmaker(data)
        await ctx.send(embed=em)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild:
            items = re.search(r"\[(\w+)\]", message.content)
            if items
                for item in items:
                    data = await self.itemlookup(item)
                    em = await self.embedmaker(data)
                    await ctx.send(embed=em)

    async def itemlookup(self, item):
        data = await (await self.session.get(f"https://api.nexushub.co/wow-classic/v1/item/{item}")).json()
        return data
        
    async def embedmaker(self, data):
        if "error" in data:
            return
        
        tooltip_data = data["tooltip"]
        
        labels = []

        for label in tooltip_data:
            labels.append(label["label"])
        
        em = discord.Embed(title=data["name"], description="\n".join(labels[1:-1]), url=f"https://classic.wowhead.com/item={data['itemId']}", colour=0xff0000)
        em.set_thumbnail(url=data["icon"])

        return em
