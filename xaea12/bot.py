import os
import sys
import random

import discord
from discord.ext import commands

from .core.loader import Loader
from .core.checks import owner_permissions

class XAEA12Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        intents = discord.Intents.all()

        super().__init__(*args, **kwargs, intents=intents)

        self.command_prefix = kwargs.get('command_prefix', 'x!')
        self.activities = ['TECHNOBLADE NEVER DIES!', 'Technoblade vs Dream', 'Technoblade\'s bed wars streams']
        self.loader = Loader(self)
        path = os.path.join('xaea12', 'cogs')
        self.modules = Loader.get_modules(path)

    @staticmethod
    @commands.command(name='restart')
    @owner_permissions()
    async def restart(ctx):
        """Command to restart bot."""
        await ctx.send('Restarting...')
        os.execl(sys.executable, sys.executable, *sys.argv)

    async def on_ready(self):
        for attr in self.__dir__():
            attr = getattr(self, attr)
            if callable(attr) and isinstance(attr, commands.Command):
                self.add_command(attr)

        for filename in self.modules:
            self.loader.load_module(filename)

        activity = discord.Activity(type=discord.ActivityType.watching, name=random.choice(self.activities))
        await self.change_presence(status=discord.Status.online, activity=activity)

        print('Logged in as')
        print('login: {}'.format(self.user.name))
        print('id: {}'.format(self.user.id))
        print('prefix: {}'.format(self.command_prefix))
        print('Connected.')

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        ctx = await self.get_context(message)
        if message.content.startswith(self.command_prefix):
            await self.invoke(ctx)

    async def on_member_join(self, member: discord.Member):
        if member.guild.system_channel is not None:
            await member.guild.system_channel.send('Welcome {0.mention}!'.format(member))

    async def on_member_remove(self, member: discord.Member):
        if member.guild.system_channel is not None:
            await member.guild.system_channel.send('{0.name} has gone.'.format(member))

    async def on_command_error(self, ctx: commands.Context, error):
        await ctx.send(error)

    def run(self, *args):
        self.loop.run_until_complete(self.start(*args))
        self.loop.close()
