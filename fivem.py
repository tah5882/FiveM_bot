import discord
import os
from group.admin import admin
from group.fivem import fivem
from cogs2.update import update
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

token = os.getenv("TOKEN")

class MyBot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    async def setup_hook(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'Loaded extension: {filename[:-3]}')
        for filename in os.listdir('./event'):
            if filename.endswith('.py'):
                await bot.load_extension(f'event.{filename[:-3]}')
                print(f'Loaded extension: {filename[:-3]}')
        await bot.add_cog(update(bot))

intents = discord.Intents.all()
bot = MyBot(intents=intents,command_prefix="$",case_insensitive=True)
tree = bot.tree

@bot.event
async def on_ready():
    print('-----')
    print(bot.user.name)
    print(bot.user.id)
    print('-----')
    print(f'Login {bot.user}')
    print(discord.__version__)
    tree.add_command(admin("admin"))
    tree.add_command(fivem("fivem"))
    await tree.sync()

@tree.command(name="reload",description="コマンドをリロードします(Admin only)")
async def reload(interaction: discord.Interaction, extension: str):
    if interaction.user.id != 756728239673573376:
        return
    try:
        await bot.reload_extension(extension)
        await interaction.response.send_message(f'Reloaded extension: {extension}',ephemeral=False)
    except Exception as e:
        await interaction.response.send_message(f'Error reloading extension: {extension}\n{type(e).__name__}: {str(e)}',ephemeral=True)
        
@tree.command(name="stop",description="Botを停止します(Admin only)")
async def stop(interaction: discord.Interaction):
    if interaction.user.id != 756728239673573376:
        return
    await interaction.response.send_message("Botを停止します",ephemeral=True)
    await bot.close()

bot.run(token)

