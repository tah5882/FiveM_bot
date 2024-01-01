import discord
import json
from discord import app_commands
from discord.ext import commands

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

class admin(app_commands.Group):
    def __init__(self, bot, **kwargs):
        super().__init__(**kwargs)
        self.bot = bot

    @app_commands.command(name="support_setup")
    @commands.has_permissions(administrator=True)
    @app_commands.choices(args=[
        discord.app_commands.Choice(name="fivem", value="fivem"),
        discord.app_commands.Choice(name="minecraft", value="minecraft")
    ])
    async def setup(self, interaction: discord.Interaction, args: str):
        if args == "fivem":
            embed = discord.Embed(title="Status",description="loading...",)
            m = await interaction.channel.send(embed=embed)
            with open('data/config.json', 'r') as file:
                data = json.load(file)
            data['m_id1'] = m.id
            data['c_id1'] = interaction.channel.id
            with open('data/config.json', 'w') as file:
                json.dump(data, file)
            await interaction.response.send_message("セットアップが完了しました", ephemeral=True)
        elif args == "minecraft":
            embed = discord.Embed(title="Status",description="loading...",)
            m = await interaction.channel.send(embed=embed)
            with open('data/config.json', 'r') as file:
                data = json.load(file)
            data['m_id2'] = m.id
            data['c_id2'] = interaction.channel.id
            with open('data/config.json', 'w') as file:
                json.dump(data, file)
            await interaction.response.send_message("セットアップが完了しました", ephemeral=True)
        else:
            await interaction.response.send_message("引数が不正です", ephemeral=True)
    
    @setup.error
    async def on_daily_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("権限が不足しています", ephemeral=True)
