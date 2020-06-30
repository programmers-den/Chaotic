@bot.command()
async def say(ctx, *, args=None):
    if args == None:
        pass
    else:
        ctx.send(args)