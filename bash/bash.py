import discord
from redbot.core import checks, commands
import os
import subprocess
import sys
import asyncio
from subprocess import Popen
import threading
from asyncio.subprocess import PIPE, STDOUT
from redbot.core.utils.chat_formatting import pagify

BaseCog = getattr(commands, "Cog", object)

class Bash(BaseCog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=["shell"])
    @checks.is_owner()
    async def bash(self, ctx, *, arg):
        """Bash shell"""
        env = os.environ.copy()
        if hasattr(sys, "real_prefix") or sys.base_prefix != sys.prefix:
            # os.path.sep - this is folder separator, i.e. `\` on win or `/` on unix
            # os.pathsep - this is paths separator in PATH, i.e. `;` on win or `:` on unix
            if sys.platform == "win32":
                binfolder = f"{sys.prefix}{os.path.sep}Scripts"
                env["PATH"] = f"{binfolder}{os.pathsep}{env['PATH']}"
            else:
                binfolder = f"{sys.prefix}{os.path.sep}bin"
                env["PATH"] = f"{binfolder}{os.pathsep}{env['PATH']}"

        proc = await asyncio.create_subprocess_shell(arg, stdin=None, stderr=STDOUT, stdout=PIPE, env=env)
        out = await proc.stdout.read()
        msg = pagify(out.decode('utf-8'))
        await ctx.send(f"```ini\n\n[Bash Input]: {arg}\n```")
        await ctx.send_interactive(msg, box_lang="py")
