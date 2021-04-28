import datetime

from discord.ext import commands
from ..core.cog import Cog

class LOL(Cog):
    @commands.command()
    async def today(self, ctx: commands.Context):
        """Command that prints what day is today"""

        weekday = datetime.datetime.today().weekday()
        weekdays = ['Monday', 'Tuesaday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        await ctx.send('Today is {}'.format(weekdays[weekday]))

def setup(bot: commands.Bot):
    bot.add_cog(LOL(bot))
