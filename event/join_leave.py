async def setup(bot):
    import discord

    @bot.listen("on_member_join")
    async def join_message(member:discord.Member):
        embed = discord.Embed(description=f"{member.mention}さんが参加しました！",color=discord.Colour.green())
        embed.set_footer(text=f"参加者数：{len(member.guild.members)}人")
        await member.guild.get_channel(1190627773274935357).send(embed=embed)
    
    @bot.listen("on_member_remove")
    async def leave_message(member:discord.Member):
        embed = discord.Embed(description=f"{member.mention}さんが退出しました...",color=discord.Colour.red())
        embed.set_footer(text=f"参加者数：{len(member.guild.members)}人")
        await member.guild.get_channel(1190627773274935357).send(embed=embed)