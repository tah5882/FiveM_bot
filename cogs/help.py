async def setup(bot):
    import discord
    from discord import app_commands

    tree = bot.tree

    @tree.command(name="help",description="helpページ")
    @app_commands.describe(commands="特定のコマンドのhelpを表示します")
    @app_commands.choices(
        commands = [
            discord.app_commands.Choice(name="ping", value="ping"),
        ]
    )
    async def help(interaction:discord.interactions,commands:str = None):
        if commands == "ping":
            embed = discord.Embed(description="</ping:1147651404111028265>\nbotの速度を返します")
        else:
            embed = discord.Embed(title="help")
            embed.add_field(name="ping",value="</ping:1147651404111028265>\nbotの速度を返します")
        

        button = discord.ui.Button(label="Delete",style=discord.ButtonStyle.red,custom_id="delete")
        view = discord.ui.View()
        view.add_item(button)

        await interaction.response.send_message(embed=embed,view=view)


    @bot.listen('on_interaction')
    async def interaction(inter:discord.Interaction):
        try:
            if inter.data['component_type'] == 2:
                await on_button_click1(inter)
        except KeyError:
            pass

    async def on_button_click1(inter:discord.Interaction):
        custom_id = inter.data["custom_id"]
        if custom_id == "delete":
                await inter.message.delete()
                await inter.message.delete()