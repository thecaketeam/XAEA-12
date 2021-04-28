import discord
from discord.ext import commands

from ..core.checks import has_permissions
from ..core.cog import Cog

class Moderator(Cog):
    @commands.command(usage='<member>')
    @has_permissions(manage_roles=True)
    async def mute(self, ctx: commands.Context, member: discord.Member):
        """Command to mute server member"""

        role = discord.utils.get(ctx.guild.roles, name='mute')
        if role is None:
            permissions = discord.Permissions(send_messages=False, read_messages=True, read_message_history=True)
            role = await ctx.guild.create_role(name='mute', color=discord.Colour.dark_magenta, permissions=permissions)

        await member.add_roles(role)

    @commands.command(usage='<member>')
    @has_permissions(manage_roles=True)
    async def unmute(self, ctx: commands.Context, member: discord.Member):
        """Command to unmute server member"""

        role = discord.utils.get(ctx.guild.roles, name='mute')
        if role is None:
            return

        await member.remove_roles(role)

    @commands.command(usage='<number of messages>')
    @has_permissions(manage_channels=True)
    async def clear(self, ctx: commands.Context, limit=1):
        """Command to delete last N messages"""

        await ctx.channel.purge(limit=limit)

    @commands.command(usage='<member> <reason>')
    @has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, member: discord.Member=None, *, reason):
        """Command to kick user from server"""

        if member is None:
            return

        await member.kick(reason=reason)

def setup(bot: commands.Bot):
    bot.add_cog(Moderator(bot))
