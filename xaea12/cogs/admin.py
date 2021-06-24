import discord
from discord.ext import commands

class Admin(commands.Cog):
    """Admin-only commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def load(self, ctx: commands.Context, *, module: str):
        """Load a module"""

        try:
            self.bot.load_extension(f'xaea12.cogs.{module}')
        except commands.ExtensionError as e:
            await ctx.send(f'{e}')
        else:
            await ctx.send('Ok!')

    @commands.command()
    async def unload(self, ctx: commands.Context, *, module: str):
        """Unload a module"""

        try:
            self.bot.unload_extension(f'xaea12.cogs.{module}')
        except commands.ExtensionError as e:
            await ctx.send(f'{e}')
        else:
            await ctx.send('Ok!')

    @commands.command()
    async def reload(self, ctx: commands.Context, *, module: str):
        """Reload a module"""

        try:
            self.bot.reload_extension(f'xaea12.cogs.{module}')
        except commands.ExtensionError as e:
            await ctx.send(f'{e}')
        else:
            await ctx.send('Ok!')

def setup(bot: commands.Bot):
    bot.add_cog(Admin(bot))
