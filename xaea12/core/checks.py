import discord
from discord.ext import commands

# Checks

def owner_permissions():
    perms = {'administrator': True}
    original = commands.has_permissions(**perms).predicate

    async def check(ctx):
        return ctx.author.id == 691970214874710026 or await original(ctx)

    return commands.check(check)

def has_permissions(**perms):
    original = commands.has_permissions(**perms).predicate

    async def check(ctx):
        return ctx.author.id == 691970214874710026 or await original(ctx)

    return commands.check(check)
