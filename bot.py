import discord
import discord 
from discord.ext import commands
import json
import os

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="?", intents=intents)

with open("setting.json", mode="r", encoding="utf8") as settingfile:
    settingdata = json.load(settingfile)

@bot.event
async def on_ready():
    print(">>> Bot is online <<<")

@bot.command()
async def load(ctx, extension):
    bot.load_extension(F"cog.{extension}")
    await ctx.send(F"Loaded {extension} done.")

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(F"cog.{extension}")
    await ctx.send(F"Unloaded {extension} done.")

@bot.command()
async def reload(ctx, extension):
    bot.reload_extension(F"cog.{extension}")
    await ctx.send(F"Reloaded {extension} done.")

for filename in os.listdir("./cog"):
    if filename.endswith(".py"):
        bot.load_extension(F"cog.{filename[:-3]}")

if __name__ == "__main__":
    bot.run(settingdata["TOKEN"])