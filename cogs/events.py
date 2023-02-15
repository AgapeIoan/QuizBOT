import datetime
import os
import json

from disnake.ext import commands

from functii.debug import print_debug, print_log

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter, error):
        print_log(f'Error: {error}')
        
    # Listen for commands
    @commands.Cog.listener()
    async def on_slash_command(self, inter):
        options = inter.options
        print_log(options)


def setup(bot):
    bot.add_cog(Events(bot))
