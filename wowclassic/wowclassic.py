import discord, json, re, aiohttp, chromedriver_binary
from redbot.core import commands, checks, Config
from redbot.core.data_manager import cog_data_path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from PIL import Image
from os import path

BaseCog = getattr(commands, "Cog", object)

class WowClassic(BaseCog):
    def __init__(self, bot):
        self.bot = bot
        # Webdriver
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("window-size=1920x1080")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=chrome_options, executable_path=chromedriver_binary.chromedriver_filename)
        # Config
        self.config = Config.get_conf(self, identifier=3794294739172, force_registration=True)
        default_channel = {"toggle": False}
        self.config.register_channel(**default_channel)
        # Session
        self.session = aiohttp.ClientSession()

    def cog_unload(self):
        self.bot.loop.create_task(self.driver.quit())
        self.bot.loop.create_task(self.session.close())

    @commands.group()
    @commands.guild_only()
    async def classic(self, ctx):
        """WoW Classic"""
        pass

    @classic.command()
    async def search(self, ctx, *, query):
        """Tooltip data search"""
        item = await self._name_lookup(query)
        if item == "no match":
            await ctx.send(":x: Unable to find an item with that name.")
            return
        image_path = str(cog_data_path(self) / f"{item}.png")
        url = f"https://classic.wowhead.com/item={item}"
        if path.isfile(image_path):
            await ctx.send(f"<{url}>", file=discord.File(image_path))
        else:
            image_path = await self._generate_tooltip(item)
            await ctx.send(f"<{url}>", file=discord.File(image_path))

    @classic.command()
    @checks.mod_or_permissions(administrator=True)
    async def toggle(self, ctx):
        """Toggle command-less queries in current channel"""
        current = await self.config.channel(ctx.channel).toggle()
        if current == False:
            await self.config.channel(ctx.channel).toggle.set(True)
            await ctx.send(f"{ctx.channel.mention} has been enabled.")
        else:
            await self.config.channel(ctx.channel).toggle.set(False)
            await ctx.send(f"{ctx.channel.mention} has been disabled.")

    @commands.Cog.listener()
    async def on_message(self, message):
        current = await self.config.channel(message.channel).toggle()
        if current == True:
            items = re.findall(r"[^[]*\[([^]]*)\]", message.content)
            if items:
                items = list(dict.fromkeys(items))[:3]
                for item in items:
                    item = await self._name_lookup(item)
                    if item == "no match":
                        continue
                    image_path = str(cog_data_path(self) / f"{item}.png")
                    url = f"https://classic.wowhead.com/item={item}"
                    if path.isfile(image_path):
                        await message.channel.send(f"<{url}>", file=discord.File(image_path))
                    else:
                        image_path = await self._generate_tooltip(item)
                        await message.channel.send(f"<{url}>", file=discord.File(image_path))

    async def _name_lookup(self, query):
        async with self.session.get(f"https://api.nexushub.co/wow-classic/v1/search?query={query}&limit=1") as resp:
            item = await resp.content.read()
            try:
                item_id = json.loads(item)[0]["itemId"]
                return item_id
            except IndexError:
                return "no match"

    async def _generate_tooltip(self, item_id):
        image_path = str(cog_data_path(self) / f"{item_id}.png")
        
        css = '<link rel="stylesheet" type="text/css" href="https://wow.zamimg.com/css/classic/basic.css"><style type="text/css">body {background-color: black}</style>'

        url = f"https://classic.wowhead.com/item={item_id}"
        
        self.driver.get(url)

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        tooltip_data = soup.find("div", attrs={"class": "wowhead-tooltip"})
        complete_tooltip = f"data:text/html;charset=utf-8,{css}{tooltip_data}"

        self.driver.get(complete_tooltip)

        element = self.driver.find_element_by_tag_name("table");
        location = element.location;
        size = element.size;

        self.driver.save_screenshot(image_path)

        x = location['x'];
        y = location['y'];
        width = location['x']+size['width'];
        height = location['y']+size['height'];
        im = Image.open(image_path)
        im = im.convert("RGBA")
        im = im.crop((int(x), int(y), int(width), int(height)))
        datas = im.getdata()
        newData = []
        for item in datas:
            if item[0] == 0 and item[1] == 0 and item[2] == 0:
                newData.append((0, 0, 0, 0))
            else:
                newData.append(item)
        im.putdata(newData)
        im.save(image_path, optimize=True)
        return image_path
