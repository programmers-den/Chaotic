import discord
import os
from discord.ext import commands

prefix = os.environ.get("PREFIX")
token = os.environ.get("TOKEN")
bot = commands.AutoShardedBot(command_prefix=prefix, case_insensitive=True)

@bot.event
async def on_ready():
    print("Python: Ready!")

for command in os.listdir("commands"):
    if command.endswith('.py'):
        with open(f"commands/{command}") as f:
            exec(f.read())

bot.run(token)