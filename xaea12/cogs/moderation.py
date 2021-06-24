import discord
from discord.ext import commands

class Moderation(commands.Cog):
    """Moderator commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=False)
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx: commands.Context, member: discord.Member):
        """Mute a guild member"""

        role = None
        while role is None:
            permissions = discord.Permissions(send_messages=False, read_messages=True)
            role = await ctx.guild.create_role(name='mute', color=discord.Colour.dark_magenta, permissions=permissions)

        await member.add_roles(role)

    @commands.command(hidden=False)
    @commands.has_permissions(manage_roles=True)
    async def ummute(self, ctx: commands.Context, member: discord.Member):
        """Unmute a guild member"""

        role = discord.utils.get(ctx.guild.roles, name='mute')
        if role is None:
            return

        await member.remove_roles(role)

    @commands.command(hidden=False)
    @commands.has_permissions(manage_channels=True)
    async def clear(self, ctx: commands.Context, limit: int = 1):
        """Delete last N messages"""

        await ctx.channel.purge(limit=limit)

    @commands.command(hidden=False)
    @commands.has_permissions(create_instant_invite=True)
    async def createinvite(self, ctx: commands.Context):
        """Create an invite link to the channel"""

        invite = await ctx.channel.create_invite(unique=True)
        await ctx.send(f"Here's your invite: {invite}")

    @commands.command(hidden=False)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, member: discord.Member, *, reason: str):
        """Kick a guild member"""

        if member is None:
            await ctx.send("Failed!")
            return

        await member.kick(reason=reason)
        await ctx.send(f"{member} have been kicked")

    @commands.command(hidden=False)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, member: discord.Member, *, reason: str):
        """Ban a guild member"""

        if member is None:
            await ctx.send("Failed!")
            return

        await member.ban(reason=reason)
        await ctx.send(f"{member} have been banned")

    @commands.command(hidden=False)
    @commands.has_permissions(kick_members=True)
    async def unban(self, ctx: commands.Context, member: str):
        """Unban a member"""

        if member is None:
            await ctx.send("Failed!")
            return

        member_name, member_discriminator = member.split('#')
        banned = await ctx.guild.bans()
        for ban in banned:
            user = ban.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"{member} have been unbanned")
                return

def setup(bot: commands.Bot):
    bot.add_cog(Moderation(bot))
