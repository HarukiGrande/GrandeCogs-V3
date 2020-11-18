from .wowclassic import WowClassic

def setup(bot):
    bot.add_cog(WowClassic(bot))