import discord, aiohttp, re, selenium
from redbot.core import commands
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
from bs4 import BeautifulSoup
from chromedriver_py import binary_path
import urllib.parse
from redbot.core.data_manager import cog_data_path

BaseCog = getattr(commands, "Cog", object)

class WowClassic(BaseCog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)
        
    @commands.group()
    @commands.guild_only()
    async def classic(self, ctx):
        """WoW Classic"""
        pass
        
    @classic.command()
    async def lookup(self, ctx, *, name):
        """WoWHead Lookup"""
        name = urllib.parse.quote(name)
        status = await self.wowhead_image_gen(name)
        if status == "single":
            await ctx.send(file=discord.File(cog_data_path(self) / f"{name}.png"))
        else:
            await ctx.send(f"Unable to find {name}.")

    async def wowhead_image_gen(self, name):
        css_source = '<link rel="stylesheet" type="text/css" href="https://wow.zamimg.com/css/classic/basic.css"><link rel="stylesheet" type="text/css" href="https://wow.zamimg.com/css/classic/global.css"><link rel="stylesheet" type="text/css" href="https://wow.zamimg.com/css/themes/classic.css"><link rel="stylesheet" type="text/css" href="https://wow.zamimg.com/css/classic/tools/book.css">'

        url = f"https://classic.wowhead.com/search?q={name}"

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=binary_path)
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        html_source = soup.find("div", attrs={"class": "wowhead-tooltip"})

        html_source = 'data:text/html;charset=utf-8,' + css_source + str(html_source)

        driver.get(html_source)

        try:
            element = driver.find_element_by_tag_name("table");
            location = element.location;
            size = element.size;

            driver.save_screenshot(str(cog_data_path(self) / f"{name}.png"))

            x = location['x'];
            y = location['y'];
            width = location['x']+size['width'];
            height = location['y']+size['height'];
            im = Image.open(str(cog_data_path(self) / f"{name}.png"))
            im = im.crop((int(x), int(y), int(width), int(height)))
            im.save(str(cog_data_path(self) / f"{name}.png"))
            driver.quit()
            return "single"
    
        except selenium.common.exceptions.NoSuchElementException:
            return "no"
