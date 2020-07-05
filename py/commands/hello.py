@bot.command()
async def hello(ctx):
    await ctx.message.delete()
    await ctx.send("Hi! I'm alive :heart:")
