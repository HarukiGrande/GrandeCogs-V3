from .nexushub import NexusHub

def setup(bot):
    bot.add_cog(NexusHub(bot))