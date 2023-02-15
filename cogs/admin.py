import json
import functii.bools as bools

from disnake.ext import commands
from functii.debug import print_log
from functii.sql import send_data_to_db

class Admins(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(bools.is_dev)
    async def load(self, ctx, name: str):
        """ Loads an extension. """
        try:
            self.bot.load_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(f"```py\n{e}\n```")
        await ctx.send(f"Loaded extension **{name}.py**")
        print_log(f"Loaded extension **{name}.py**")

    @commands.command()
    @commands.check(bools.is_dev)
    async def unload(self, ctx, name: str):
        """ Unloads an extension. """
        try:
            self.bot.unload_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(f"```py\n{e}\n```")
        await ctx.send(f"Unloaded extension **{name}.py**")
        print_log(f"Unloaded extension **{name}.py**")

    @commands.command()
    @commands.check(bools.is_dev)
    async def reload(self, ctx, name: str):
        """ Reloads an extension. """
        try:
            self.bot.reload_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(f"```py\n{e}\n```")
        await ctx.send(f"Reloaded extension **{name}.py**")
        print_log(f"Reloaded extension **{name}.py**")

def setup(bot):
    bot.add_cog(Admins(bot))