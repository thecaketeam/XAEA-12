import os
import sys
import random

import discord
from discord.ext import commands

from .config import Config

class XAEA12(commands.Bot):
    def __init__(self, name="config.json"):
        intents = discord.Intents.all()

        self.config = Config(name)
        self.prefix = self.config.get('prefix', 'x!')
        self.shard_count = self.config.get('shard_count', 2)

        super().__init__(command_prefix=self.prefix, case_insensitive=True,
                         heartbeat_timeout=150.0, shard_count=self.shard_count,
                         fetch_offline_members=False, intents=intents)

        self.greeting_message = self.config.get('greeting_message', 'Welcome {member}!')
        self.leave_message = self.config.get('leave_message', '{member} has gone.')

        cog_path = os.path.join(os.path.dirname(__file__), 'cogs')
        self.cog_path = self.config.get('cog_path', cog_path)

        self.activities = [
            discord.Activity(type=discord.ActivityType.watching, name='Technoblade vs Dream'),
            discord.Activity(type=discord.ActivityType.watching, name='Technoblade\'s Bed Wars streams'),
        ]

    async def on_ready(self):
        print(f'Logged in as {self.user.display_name} (ID: {self.user.id})')

        activity = random.choice(self.activities)
        await self.change_presence(status=discord.Status.online, activity=activity)

        self.add_command(XAEA12._restart)
        for filename in os.listdir(self.cog_path):
            base, ext = os.path.splitext(filename)
            if ext == '.py':
                cog = 'xaea12.cogs.{}'.format(base)
                self.load_extension(cog)

    async def on_command_error(self, ctx: commands.Context, exception: Exception):
        await ctx.send(exception)

    async def on_member_join(self, member: discord.Member):
        if member.guild.system_channel is not None:
            message = self.greeting_message.format(member=member.mention)
            await member.guild.system_channel.send(message)

    async def on_member_remove(self, member: discord.Member):
        if member.guild.system_channel is not None:
            message = self.leave_message.format(member=member.mention)
            await member.guild.system_channel.send(message)

    def run(self, *args, **kwargs):
        try:
            self.loop.run_until_complete(self.start(self.config.get('token', os.getenv('DISCORD_TOKEN')), *args, **kwargs))
        except KeyboardInterrupt:
            self.loop.run_until_complete(self.close())
        except (AttributeError, discord.errors.LoginFailure):
            print("Invalid token!")
        finally:
            self.loop.close()

    @staticmethod
    @commands.command(name='restart')
    @commands.has_permissions(administrator=True)
    async def _restart(ctx: commands.Context):
        """Restart bot"""

        await ctx.send('Restarting...')
        os.execl(sys.executable, sys.executable, *sys.argv)
