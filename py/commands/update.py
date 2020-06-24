@bot.command()
async def update(ctx):
    data = 524288464422830095, 524288464422830095, 207188318130012160, 562086061153583122
    if ctx.author.id in data:
        await ctx.send("Request Received, Rebooting in 10 second")
        await asyncio.sleep(10)
        try:
            os.system("../stop.sh")
        except:
            await ctx.send("ERR")