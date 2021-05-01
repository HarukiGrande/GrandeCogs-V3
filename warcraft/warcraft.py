import discord, aiohttp
from redbot.core import commands, checks, Config

BaseCog = getattr(commands, "Cog", object)

class Warcraft(BaseCog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())

    @commands.group()
    @commands.guild_only()
    async def warcraft(self, ctx):
        """Warcraft"""
        pass
    
    @warcraft.command()
    async def profile(self, ctx, region, realm, character):
        region_safe = await self._check_region_exists(region)
        if region_safe is False:
            return await ctx.send("Invalid region.")
        url_profile = (f"https://{region}.api.blizzard.com/profile/wow/character/{realm}/{character}?namespace=profile-{region}".lower())+"&locale=en_GB"
        url_image = (f"https://{region}.api.blizzard.com/profile/wow/character/{realm}/{character}/character-media?namespace=profile-{region}".lower())+"&locale=en_GB"
        url_mounts = (f"https://{region}.api.blizzard.com/profile/wow/character/{realm}/{character}/collections/mounts?namespace=profile-{region}".lower())+"&locale=en_GB"
        url_pets = (f"https://{region}.api.blizzard.com/profile/wow/character/{realm}/{character}/collections/pets?namespace=profile-{region}".lower())+"&locale=en_GB"
        profile = await self._api_call(url_profile)
        if profile == "invalid":
            return await ctx.send("Invalid client tokens.")
        if "code" in profile:
            if profile["code"] == 404:
                return await ctx.send("Character not found.")
        image = await self._api_call(url_image)
        if "active_title" in profile:
            title = str(profile["active_title"]["display_string"])
        else:
            title = "{name}"
        if profile["faction"]["type"] == "HORDE":
            faction_colour = discord.Colour.from_rgb(189,31,31)
        if profile["faction"]["type"] == "ALLIANCE":
            faction_colour = discord.Colour.from_rgb(31,89,189)
        em = discord.Embed(title=title.format(name=profile["name"]), description=f"Level {profile['level']} {profile['race']['name']} {profile['character_class']['name']} ({profile['active_spec']['name']})", url=f"https://worldofwarcraft.com/character/{region}/{realm}/{character}", colour=faction_colour)
        if "code" not in image:
            em.set_thumbnail(url=image["assets"][0]["value"])
        if "guild" in profile:
            em.add_field(name="Guild", value=profile["guild"]["name"], inline=False)
        if "covenant_progress" in profile:
            em.add_field(name="Covenant", value=f"{profile['covenant_progress']['chosen_covenant']['name']} ({profile['covenant_progress']['renown_level']} Renown)", inline=False)
        em.add_field(name="Item Level", value=profile["average_item_level"], inline=False)
        em.add_field(name="Achievement Points", value=profile["achievement_points"], inline=False)
        mounts = await self._api_call(url_mounts)
        if "code" not in mounts:
            em.add_field(name="Mounts", value=len(mounts["mounts"]))
        pets = await self._api_call(url_pets)
        em.add_field(name="Pets", value=len(pets["pets"]))
        await ctx.send(embed=em)

    async def _generate_access_token(self):
        client_tokens = await self.bot.get_shared_api_tokens("battlenet")
        if client_tokens.get("client_id") is None:
            return "invalid"
        client_id = client_tokens.get("client_id", "")
        client_secret = client_tokens.get("client_secret", "")
        async with aiohttp.ClientSession(auth=aiohttp.BasicAuth(login=client_id, password=client_secret)) as session:
            form = aiohttp.FormData()
            form.add_field("grant_type", "client_credentials")
            request = await session.post("https://us.battle.net/oauth/token", data=form)
            access_token = await request.json()
        return access_token.get("access_token")
        
    async def _api_call(self, url):
        access_token = await self._generate_access_token()
        if access_token == "invalid":
            return "invalid"
        data = {
            "accept": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        async with self.session.get(url, headers=data) as resp:
            json_data = await resp.json()
        return json_data
    
    async def _check_region_exists(self, region):
        regions = ["us","eu","kr","tw","cn"]
        for item in regions:
            if region == item:
                return True
        return False
