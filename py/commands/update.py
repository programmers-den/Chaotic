@bot.command()
async def update(ctx):
    role = ctx.guild.get_role(725512500220657674)
    if role in ctx.author.roles:
        await ctx.send("Request Received, Rebooting in 10 second")
        await asyncio.sleep(10)
        try:
            os.system("../stop.sh")
        except:
            await ctx.send("ERR")