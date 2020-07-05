@bot.command()
async def test(ctx):
    await ctx.message.delete()
    await ctx.send("PY: Test successful")
