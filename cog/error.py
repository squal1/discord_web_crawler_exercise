import discord
import json
from discord.ext import commands
import os
from core.classes import Cog_Extension

class Error(Cog_Extension):
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("MissingRequiredArgument")
        elif isinstance(error, commands.errors.CommandNotFound):
            embed=discord.Embed(color=0xff0000)
            embed.add_field(name="Error", value="Cannot find the command", inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send(error)

def setup(bot):
    pass
#    bot.add_cog(Error(bot))