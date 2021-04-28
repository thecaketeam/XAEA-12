from discord.ext import commands
from ..core.checks import owner_permissions
from ..core.cog import Cog

class Admin(Cog):
    @commands.command(usage='<module>')
    @owner_permissions()
    async def load(self, ctx: commands.Context, name=None):
        """Command to load new modules"""

        if name is not None:
            self.bot.loader.load_module(name)
        else:
            print("Invalid module name")

    @commands.command(usage='<module>')
    @owner_permissions()
    async def unload(self, ctx: commands.Context, name=None):
        """Command to unload modules"""

        if name is not None:
            self.bot.loader.unload_module(name)
        else:
            print("Invalid module name")

    @commands.command(usage='<module>')
    @owner_permissions()
    async def reload(self, ctx: commands.Context, name=None):
        """Command to reload modules"""

        if name is not None:
            self.bot.loader.reload_module(name)
        else:
            print("Invalid module name")

    @commands.command(usage='<command prefix>')
    @owner_permissions()
    async def set_prefix(self, ctx: commands.Context, prefix=None):
        """Command to change commands prefix"""

        if prefix is not None:
            self.bot.command_prefix = prefix

def setup(bot: commands.Bot):
    bot.add_cog(Admin(bot))
