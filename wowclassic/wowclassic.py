import discord, re, selenium, json
from redbot.core import commands
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
from bs4 import BeautifulSoup
from chromedriver_py import binary_path
import urllib.parse
from redbot.core.data_manager import cog_data_path
from redbot.core.data_manager import bundled_data_path
import os.path
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
    async def tooltip(self, ctx, *, query):
        """Tooltip data search"""
        file_path = bundled_data_path(self) / "data.json"
        try:
            with file_path.open("rt") as f:
                data = json.loads(f.read())
                data_names = [item.get("name") for item in data]
                match = process.extractOne(query, data_names)[0]
                for item in data:
                    if item["name"] == match:
                        return await ctx.send(item["tooltip"])
        except FileNotFoundError:
            return await ctx.send("oops")
        await ctx.send(f"Could not find {query}.")

"""

    @classic.command()
    async def lookup(self, ctx, *, name):
        """WoWHead Lookup"""
        async with ctx.typing():
            name = urllib.parse.quote(name)
            if os.path.isfile(str(cog_data_path(self) / f"{name}.png")):
                await ctx.send(file=discord.File(str(cog_data_path(self) / f"{name}.png")))
            else:
                status = await self.wowhead_image_gen(name)
                if status == "single":
                    await ctx.send(file=discord.File(str(cog_data_path(self) / f"{name}.png")))
                else:
                    await ctx.send(f"Unable to find {name}.")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild:
            names = re.findall(r"[^[]*\[([^]]*)\]", message.content)
            if names:
                names = list(dict.fromkeys(names))
                for name in names:
                    name = urllib.parse.quote(name)
                    if os.path.isfile(str(cog_data_path(self) / f"{name}.png")):
                        await message.channel.send(file=discord.File(str(cog_data_path(self) / f"{name}.png")))
                    else:
                        status = await self.wowhead_image_gen(name)
                        if status == "single":
                            await message.channel.send(file=discord.File(str(cog_data_path(self) / f"{name}.png")))

    async def wowhead_image_gen(self, name):
        css_source = '<link rel="stylesheet" type="text/css" href="https://wow.zamimg.com/css/classic/basic.css"><link rel="stylesheet" type="text/css" href="https://wow.zamimg.com/css/classic/global.css"><link rel="stylesheet" type="text/css" href="https://wow.zamimg.com/css/themes/classic.css"><link rel="stylesheet" type="text/css" href="https://wow.zamimg.com/css/classic/tools/book.css">'

        url = f"https://classic.wowhead.com/search?q={name}"

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--incognito')
        chrome_options.add_argument('--ignore-certificate-errors')
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=binary_path)
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        html_source = soup.find("div", attrs={"class": "wowhead-tooltip"})
        
        if html_source:

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
                return "error"
        else:
            url = soup.find("a", attrs={"class": "top-results-result-link"})
            
            url = f"https://classic.wowhead.com{url.attrs['href']}"

            driver.get(url)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            html_source = soup.find("div", attrs={"class": "wowhead-tooltip"})
            
            if html_source:
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
                    return "error"
            else:
                #html_source = soup.find_all("table", attrs={"class": "infobox"})
                    
                #html_source = 'data:text/html;charset=utf-8,' + css_source + str(html_source[0])
                    
                #driver.get(html_source)

                #try:
                    #element = driver.find_element_by_tag_name("tbody");
                    #location = element.location;
                    #size = element.size;

                    #driver.save_screenshot(str(cog_data_path(self) / f"{name}.png"))

                    #x = location['x'];
                    #y = location['y'];
                    #width = location['x']+size['width'];
                    #height = location['y']+size['height'];
                    #im = Image.open(str(cog_data_path(self) / f"{name}.png"))
                    #im = im.crop((int(x), int(y), int(width), int(height)))
                    #im.save(str(cog_data_path(self) / f"{name}.png"))
                    #driver.quit()
                    #return "single"
    
                #except selenium.common.exceptions.NoSuchElementException:
                    #return "error"
                return "error"
"""
