import discord, json, re
from redbot.core import commands
from redbot.core.data_manager import bundled_data_path
from redbot.core.data_manager import cog_data_path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from chromedriver_py import binary_path
from fuzzywuzzy import process
from bs4 import BeautifulSoup
from PIL import Image
from os import path

BaseCog = getattr(commands, "Cog", object)

class WowClassic(BaseCog):
    def __init__(self, bot):
        self.bot = bot
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--incognito')
        chrome_options.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Chrome(options=chrome_options, executable_path=binary_path)

    def cog_unload(self):
        self.driver.quit()

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
        image_path = str(cog_data_path(self) / f"{item['itemId']}.png")
        if path.isfile(image_path):
            await ctx.send(file=discord.File(image_path))
        else:
            image_path = await self._generate_tooltip(item["itemId"])
            await ctx.send(file=discord.File(image_path))
    
    @commands.Cog.listener()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def on_message(self, message):
        if message.guild:
            items = re.findall(r"[^[]*\[([^]]*)\]", message.content)
            if items:
                items = list(dict.fromkeys(items))[:3]
                for item in items:
                    item = await self._name_lookup(item)
                    if item == "no match":
                        continue
                    image_path = str(cog_data_path(self) / f"{item['itemId']}.png")
                    if path.isfile(image_path):
                        await message.channel.send(file=discord.File(image_path))
                    else:
                        image_path = await self._generate_tooltip(item["itemId"])
                        await message.channel.send(file=discord.File(image_path))

    async def _name_lookup(self, query):
        file_path = bundled_data_path(self) / "data.json"
        with file_path.open("rt") as f:
            data = json.loads(f.read())
            data_names = [item.get("name") for item in data]
            match = process.extractOne(query, data_names)[0]
            perc = process.extractOne(query, data_names)[1]
            if perc >= 75:
                for item in data:
                    if item["name"] == match:
                        return item
            else:
                return "no match"

    async def _generate_tooltip(self, item_id):
        image_path = str(cog_data_path(self) / f"{item_id}.png")
        
        css = '<link rel="stylesheet" type="text/css" href="https://wow.zamimg.com/css/classic/basic.css"><link rel="stylesheet" type="text/css" href="https://wow.zamimg.com/css/classic/global.css"><link rel="stylesheet" type="text/css" href="https://wow.zamimg.com/css/themes/classic.css"><link rel="stylesheet" type="text/css" href="https://wow.zamimg.com/css/classic/tools/book.css">'

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
        im = im.crop((int(x), int(y), int(width), int(height)))
        im.save(image_path, optimize=True)
        return image_path
