from .warcraft import Warcraft

def setup(bot):
    bot.add_cog(Warcraft(bot))
