import discord, json
from redbot.core import commands
from redbot.core.data_manager import bundled_data_path
from fuzzywuzzy import process

BaseCog = getattr(commands, "Cog", object)

class WowClassic(BaseCog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.guild_only()
    async def classic(self, ctx):
        """WoW Classic"""
        pass
    
    @classic.command()
    async def search(self, ctx, *, query):
        """Tooltip data search"""
        item = await self._name_lookup(query)
        await ctx.send(item)
        
    async def _name_lookup(self, query):
        file_path = bundled_data_path(self) / "data.json"
        with file_path.open("rt") as f:
            data = json.loads(f.read())
            data_names = [item.get("name") for item in data]
            match = process.extractOne(query, data_names)[0]
            for item in data:
                if item["name"] == match:
                    return item
