import discord
import os
import json
import aiohttp
from datetime import datetime
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(intents=intents,command_prefix="$")
IP = os.getenv("IP")

beta = False
class fivem(app_commands.Group):
    def __init__(self, bot, **kwargs):
        super().__init__(**kwargs)
        self.bot = bot
    
    @app_commands.command(name="status",description="稼働状況の送信")
    @app_commands.choices(option=[
        discord.app_commands.Choice(name="オンライン", value="オンライン"),
        discord.app_commands.Choice(name="オフライン", value="オフライン"),
        discord.app_commands.Choice(name="作業", value="作業中") 
    ])
    async def status(self,interaction:discord.Interaction, option:str):
        try:
            if discord.utils.get(interaction.user.roles, id=1157249124605906945):
                with open('data/status.json', 'r') as file:
                    data = json.load(file)
                if option == "オンライン":
                    embed = discord.Embed(title="🟢参加可能",description="サーバー参加可能です",color=discord.Colour.green())
                    data['work'] = "false"
                elif option == "作業中":
                    embed = discord.Embed(title="⛔作業中",description="現在サーバー作業中です\n許可なきものの立ち入りを禁ずる",color=discord.Colour.yellow())
                    data['work'] = "true"
                with open('data/status.json', 'w') as file:
                    json.dump(data, file)
                if beta:
                    guild = bot.get_guild(1157247513854738462)
                    with open('data/config.json', 'r') as file:
                        data = json.load(file)
                    channel = guild.get_channel(data['c_id1'])
                    message = await channel.fetch_message(data['m_id1'])
                    url = f'http://{IP}/players.json'
                    try:
                        async with aiohttp.ClientSession() as session:
                            async with session.get(url) as response:
                                if response.json != "[]":
                                    player_count = range(len(response.json[0]))
                                    for item in data:
                                        name = item["name"]
                                        id = item["id"]
                                        ping = item["ping"]
                                        discord_id = [identifier.split(":")[1] for identifier in item["identifiers"] if identifier.startswith("discord")]
                                        if discord_id:
                                            user_id = f'{discord_id[0]}'
                                            user = await bot.fetch_user(user_id)
                                            description = f'{description}> `[{id}]`{name}{user.mention}\n'
                                        else:
                                            description = f'{description}> `[{id}]`{name}\n'
                                else:
                                    description = ""
                                if description == "":
                                    description = ""
                                else:
                                    description = f'**__Player list__**\n{description}'
                    except Exception as e:
                        description = ""
                    url = f'http://{IP}/info.json'
                    try:
                        async with aiohttp.ClientSession() as session:
                            async with session.get(url) as response:
                                if response.status == 200:
                                    data = response.json()
                                    max_player = data["vars"]["sv_maxClients"]
                                    print(f"max_playerを{max_player}に設定しました")
                                elif ConnectionResetError:
                                    max_player = "10"
                                    print("max_playerを10に設定しました")
                                else:
                                    max_player = "Error"
                                    print("max_playerをErrorに設定しました")
                    except Exception as e:
                        max_player = "10"
                        print("max_playerを10に設定しました")
                        print(f"定義エラー：{e}")
                    url = f'http://{IP}'
                    try:
                        async with aiohttp.ClientSession() as session:
                            async with session.get(url) as response:
                                if response.status == 200:
                                    server_status = "<:online:1183704437844344962>Online"
                                    color = discord.Colour.green()
                                else:
                                    server_status = "<:dnd:1183704436124692521>Offline"
                                    color = discord.Colour.red()
                    except Exception as e:
                        server_status = "<:dnd:1183704436124692521>Offline"
                        color = discord.Colour.red()
                        print(f"定義エラー：{e}")
                    if data['work'] == "false":
                        embed = discord.Embed(title='Server Status',description=description,color=color)
                        embed.add_field(name='Player', value=f'```[{player_count}/{max_player}]```',inline=False)
                        embed.add_field(name='Status', value=server_status,inline=False)
                        embed.set_author(name=guild.name,icon_url=guild.icon.url)
                        embed.set_footer(text=f"connect {IP}")
                        embed.timestamp = datetime.now()
                        await message.edit(embed=embed)
                        return
                    else:
                        embed = discord.Embed(title='Server Status',color=discord.Colour.yellow())
                        embed.add_field(name='Status', value=server_status,inline=False)
                        embed.set_author(name=guild.name,icon_url=guild.icon.url)
                        embed.timestamp = datetime.now()
                        await message.edit(embed=embed)
                        return
                embed.set_author(name="サーバー稼働状況")
                embed.set_footer(text=interaction.user.name,icon_url=interaction.user.display_avatar)
                channel = interaction.guild.get_channel(1157848232030908436)
                print(channel.id)
                await channel.send(embed=embed)
                await interaction.response.send_message("正常に送信されました",ephemeral=True)
            else:
                await interaction.response.send_message("あなたの権限が不足しています",ephemeral=True)
        except Exception as e:
            print(e)

    @app_commands.command(name="players",description="プレイヤーリストを表示します")
    async def players(self,interaction:discord.Interaction):
        description = ""
        url = f'http://{IP}/players.json'
        print(url)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        text = await response.text()
                        data = json.loads(text)
                        print(data)
                        color = discord.Colour.green()
                        # 情報を定義する
                        player_count = 0
                        for item in data:
                            name = item["name"]
                            id = item["id"]
                            ping = item["ping"]
                            discord_id = [identifier.split(":")[1] for identifier in item["identifiers"] if identifier.startswith("discord")]
                            player_count = len(data)
                            if discord_id:
                                user_id = f'{discord_id[0]}'
                                description = f'{description}`[{id}]`：{name} <@{user_id}> ({ping}ms)\n'
                            else:
                                description = f'{description}`[{id}]`：{name} ({ping}ms)\n'
                                pass
                        if description == "":
                            description = "接続しているプレイヤーはいません"
                    else:
                        description = "サーバーはオフラインです"
                        color = discord.Colour.red()
                    embed = discord.Embed(title="Player list",description=description,color=color)
                    embed.set_footer(text=f'合計人数:{player_count}')
                    await interaction.response.send_message(embed=embed,ephemeral=False)
        except Exception as e:
            print(e)
            await interaction.response.send_message("エラーが発生しました",ephemeral=True)