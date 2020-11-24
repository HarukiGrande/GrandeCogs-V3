from .wowclassic import WowClassic
from redbot.core import data_manager

def setup(bot):
    data_manager.load_bundled_data(WowClassic(bot), __file__)
    bot.add_cog(WowClassic(bot))
