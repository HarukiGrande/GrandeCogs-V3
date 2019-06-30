import discord, base64, re
from redbot.core import checks, commands
from redbot.core import Config
from redbot.core.data_manager import bundled_data_path
from PIL import Image, ImageDraw
from io import BytesIO

BaseCog = getattr(commands, "Cog", object)

class Sketch(BaseCog):
    def __init__(self,bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=3715378133574, force_registration=True)
        default_user = {
            "image_data": False,
            "coords": False,
        }
        self.config.register_user(**default_user)

    @commands.group()
    async def sketch(self, ctx):
        """Sketch"""
        pass

    @sketch.command()
    async def draw(self, ctx, x_coord,  y_coord, colour="#000000", width=1):
        """Draw your Sketch"""
        hex_match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', colour)
        if not hex_match:
            await ctx.send("Please use a valid hex colour.")
            return
        new_coords = (x_coord,  y_coord)
        await self._make_line(ctx.author, new_coords, colour, width)
        img = await self.config.user(ctx.author).image_data()
        await ctx.send(file=discord.File(img, "sketch.png"))

    @sketch.command()
    async def reset(self, ctx):
        """Reset your Sketch"""
        await self.config.user(ctx.author).image_data.set(False)
        await self.config.user(ctx.author).coords.set(False)
        await ctx.send("Your personal Sketch has been reset!")

    async def _make_line(self, author, new_coords, colour, width):
        sketch = await self.config.user(author).image_data()
        if sketch == False:
            sketch = bundled_data_path(self) / "sketch.png"
        else:
            sketch = BytesIO(base64.b64decode(sketch))
        im = Image.open(sketch)

        old_coords = self.config.user(author).coords()
        if old_coords == False:
            old_coords = (0, 0)

        canvas = Image.new('RGBA', (600, 400), (255, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)

        draw.line([old_coords, new_coords], fill=colour, width=width)
        im.paste(canvas, (100, 100), mask=canvas)

        img = BytesIO()
        im.save(img, "png")
        img.seek(0)
        await self.config.user(author).image_data.set(base64.b64encode(img.read()).decode())
        await self.config.user(author).coords.set(new_coords)
        return