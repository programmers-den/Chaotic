@bot.command()
async def update(ctx):
    founder = ctx.guild.get_role(int(os.environ.get("FOUNDER")))
    dev = ctx.guild.get_role(int(os.environ.get("DEV")))
    if founder in ctx.author.roles or dev in ctx.author.roles:
        await ctx.send("Request Received, Rebooting...")
        try:
            os.system("bash ../stop.sh")
        except:
            await ctx.send("ERR")