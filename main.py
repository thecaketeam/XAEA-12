import os
from xaea12.bot import XAEA12Bot

bot = XAEA12Bot(command_prefix='x!', description='XAEA-12 bot is the best')
bot.run(os.environ.get('DISCORD_TOKEN'))
