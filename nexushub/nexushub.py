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
        item = item.replace(" ", "-").replace("'", "").replace(",", "")
        data = await self.itemlookup(item)
        em = await self.tooltipembedmaker(data)
        if em == "error":
            await ctx.send(f"Unable to find {item}.")
        else:
            await ctx.send(embed=em)
    
    @nexushub.command()
    async def price(self, ctx, realm, *, item):
        """Item Lookup"""
        item = item.replace(" ", "-").replace("'", "").replace(",", "")
        data = await self.pricelookup(realm, item)
        em = await self.tooltipembedmaker(data)
        if em == "error":
            await ctx.send(f"Unable to find {item}.")
        else:
            await ctx.send(embed=em)
            em = await self.priceembedmaker(data)
            await ctx.send(embed=em)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild:
            items = re.findall(r"[^[]*\[([^]]*)\]", message.content)
            if items:
                items = list(dict.fromkeys(items))
                for item in items:
                    item = item.replace(" ", "-").replace("'", "").replace(",", "")
                    data = await self.itemlookup(item)
                    em = await self.tooltipembedmaker(data)
                    if em == "error":
                        pass
                    else:
                        await message.channel.send(embed=em)
    
    async def itemlookup(self, item):
        data = await (await self.session.get(f"https://api.nexushub.co/wow-classic/v1/item/{item}")).json()
        return data
    
    async def pricelookup(self, realm, item):
        data = await (await self.session.get(f"https://api.nexushub.co/wow-classic/v1/items/{realm}/{item}")).json()
        return data
    
    async def tooltipembedmaker(self, data):
        if "error" in data:
            return "error"
        
        tooltip_data = data["tooltip"]
        
        labels = []

        for label in tooltip_data:
            labels.append(label["label"])
        
        em = discord.Embed(title=data["name"], description="\n".join(labels[1:-1]), url=f"https://classic.wowhead.com/item={data['itemId']}", colour=0xff0000)
        em.set_thumbnail(url=data["icon"])

        return em
    
    async def priceembedmaker(self, data):
        em = discord.Embed(title="​", description=f"**Market Value:** {await self.goldify(data['stats']['current']['marketValue'])}\n**Historical Value:** {await self.goldify(data['stats']['current']['historicalValue'])}\n**Active Auctions:** {await self.goldify(data['stats']['current']['numAuctions'])}\n**Vendor:** {await self.goldify(data['sellPrice'])}", url=f"https://classic.wowhead.com/item={data['itemId']}", colour=0xff0000)

        return em
        
    async def goldify(self, gold):
        gold = str(gold)
        gold = f"{gold[:-4]}g {gold[-4:-2]}s {gold[-2:]}c"
        return gold
