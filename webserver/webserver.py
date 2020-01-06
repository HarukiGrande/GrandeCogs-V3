import discord
from redbot.core import checks, commands
from redbot.core import Config
from redbot.core.data_manager import bundled_data_path
from aiohttp import web
import asyncio, os
from pathlib import Path

BaseCog = getattr(commands, "Cog", object)

class WebServer(BaseCog):
    def __init__(self, bot):
        self.bot = bot
        self.host = "0.0.0.0"
        self.server = None
        self.app = web.Application()
        self.handler = None
        self.config = Config.get_conf(self, identifier=3723456754567, force_registration=True)
        self.config.register_global(port=8000)
        self.web = self.bot.loop.create_task(self._make_webserver())

    def __unload(self):
        self.web.cancel()
        asyncio.gather(runner.cleanup())

    @commands.group()
    @checks.is_owner()
    async def webserver(self, ctx):
        """WebServer"""
        pass

    @webserver.command()
    async def upload(self, ctx, folder=None):
        """Upload website files"""
        attachments = ctx.message.attachments
        if len(attachments) == 0:
            await ctx.send("No file uploaded, please upload something.")
            return
        if folder is None:
            for attachment in attachments:
                filepath = bundled_data_path(self) / attachment.filename
                await attachment.save(f"{filepath}")
        else:
            folder = bundled_data_path(self) / folder
            if not os.path.isdir(folder):
                os.makedirs(folder, exist_ok=True)
            for attachment in attachments:
                filepath = folder / attachment.filename
                await attachment.save(f"{filepath}")
        await ctx.send("New files uploaded!")

    @webserver.command()
    async def port(self, ctx, port:int):
        """Change webServer port."""
        await self.config.port.set(port)
        await ctx.send("Port updated!\nRestart to use the new port.")

    async def _make_webserver(self):
        global runner
        routes = web.RouteTableDef()

        @routes.get("/")
        async def index(request):
            try:
                filepath = bundled_data_path(self) / "index.html"
                with open(filepath) as f:
                    body = f.read()
            except:
                filepath = bundled_data_path(self) / "default.html"
                with open(filepath) as f:
                    body = f.read()
            return web.Response(text=body, content_type="text/html")

        @routes.get("/{file:.*}")
        async def index(request):
            try:
                filename = request.match_info["file"]
                if filename.endswith(".html"):
                    filepath = bundled_data_path(self) / filename
                    with open(filepath) as f:
                        body = f.read()
                    return web.Response(text=body, content_type="text/html")
                try:
                    filepath = bundled_data_path(self) / filename
                    if os.path.isfile(filepath):
                        return web.FileResponse(filepath)
                    else:
                        try:
                            filepath = bundled_data_path(self) / "index.html"
                            with open(filepath) as f:
                                body = f.read()
                        except:
                            filepath = bundled_data_path(self) / "default.html"
                            with open(filepath) as f:
                                body = f.read()
                        return web.Response(text=body, content_type="text/html")
                except:
                    try:
                        filepath = bundled_data_path(self) / "index.html"
                        with open(filepath) as f:
                            body = f.read()
                    except:
                        filepath = bundled_data_path(self) / "default.html"
                        with open(filepath) as f:
                            body = f.read()
                    return web.Response(text=body, content_type="text/html")
            except:
                try:
                    filepath = bundled_data_path(self) / "index.html"
                    with open(filepath) as f:
                        body = f.read()
                except:
                    filepath = bundled_data_path(self) / "default.html"
                    with open(filepath) as f:
                        body = f.read()
                return web.Response(text=body, content_type="text/html")

        await asyncio.sleep(10)
        app = web.Application()
        app.add_routes(routes)
        runner = web.AppRunner(app)
        await runner.setup()
        port = await self.config.port()
        site = web.TCPSite(runner, self.host, port)
        await site.start()
        print(f"[WEBSERVER] Serving on http://{self.host}:{port}")
