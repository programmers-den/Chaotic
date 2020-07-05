@bot.command()
async def say(ctx, *, args=None):
    await ctx.message.delete()
    if args: await ctx.send(args)
    else: await ctx.send("Please supply something to say!")
