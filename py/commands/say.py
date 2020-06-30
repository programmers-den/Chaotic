@bot.command()
async def say(ctx, *, args=None):
    if args: ctx.send(args)
    else: ctx.send("Please supply something to say!")
