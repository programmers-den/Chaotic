@bot.command()
async def update():
    if ctx.author.id in data:
        await ctx.send("Requset Received, Restarting bot in 5 second")
        await asyncio.sleep(5)
        os.system("../stop.sh")
    else:
        await ctx.send("Access to this command is denied.")