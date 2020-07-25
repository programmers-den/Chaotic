@bot.command()
async def info(ctx):
    await ctx.message.delete()
    embed = discord.Embed(title="Chaotic bot info", color=discord.Color.from_rgb(34,139,34))
    embed.add_field(name="Founder", value="Technisha Circuit")
    embed.add_field(name="Version", value="0.1.2")
    embed.add_field(name="Release Date", value="06/24/2020")
    embed.add_field(name="Github", value="https://github.com/Programmer-s-Organization/Chaotic")
    await ctx.send(embed=embed)
