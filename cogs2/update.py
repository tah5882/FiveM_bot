import discord
import aiohttp
import asyncio
import os
import json
from dotenv import load_dotenv
from datetime import datetime
from discord.ext import commands

load_dotenv()

maintenance = False

class update(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        if maintenance == False:
            print("メンテナンスはオフです")
            with open("data/config.json", "r") as file:
                data = json.load(file)
            with open("data/status.json", "r") as file:
                status_data = json.load(file)
            print("jsonを読み込みました")
            with open("data/config.json", "r") as file:
                data = json.load(file)
            guild = self.bot.get_guild(1190512400105996348)
            channel = self.bot.get_channel(data['c_id1'])
            message = await channel.fetch_message(data['m_id1'])
            while True:
                IP = os.getenv("IP")
                patch = os.getenv("patch")
                try:
                    print("ステータスの更新を開始しました")
                    while True:
                        print("処理中...")

                        url = f"http://{IP}/"
                        try:
                            async with aiohttp.ClientSession() as session:
                                async with session.get(url) as response:
                                    if response.status == 200:
                                        server_status = "<:online:1183704437844344962>Online"
                                        color = discord.Colour.green()
                                        print("server_statusをオンラインに設定しました")
                                    elif ConnectionResetError:
                                        server_status = "<:dnd:1183704436124692521>Offline"
                                        color = discord.Colour.red()
                                        print("server_statusをオフラインに設定しました")
                                    elif status_data["work"] == "true":
                                        server_status = "<:idle:1183704433243193354>Work"
                                        color = discord.Colour.yellow()
                                        print("server_statusを作業中に設定しました")
                                    else:
                                        server_status = "<:dnd:1183704436124692521>Offline"
                                        color = discord.Colour.red()
                                        print("server_statusをオフラインに設定しました")
                        except Exception:
                            server_status = "<:dnd:1183704436124692521>Offline"
                            color = discord.Colour.red()
                            print("server_statusをオフラインに設定しました")

                        # プレイヤー数を取得する
                        url = f'http://{IP}/players.json'
                        try:
                            async with aiohttp.ClientSession() as session:
                                async with session.get(url) as response:
                                    if await response.text() != "[]":
                                        data1 = await response.text()
                                        data = json.loads(data1)
                                        print(data)
                                        player_count = len(data)
                                        print(f"player_countを{player_count}に設定しました")
                                    elif aiohttp.ClientConnectorError:
                                        player_count = "0"
                                        print("player_countを0に設定しました")
                                    else:
                                        player_count = "Error"
                                        print("player_countをErrorに設定しました")
                        except Exception as e:
                            player_count = "0"
                            print("player_countを0に設定しました")
                            print(f"定義エラー1：{e}")

                        # サーバー情報を取得する
                        url = f"http://{IP}/info.json"
                        try:
                            async with aiohttp.ClientSession() as session:
                                async with session.get(url) as response:
                                    if response.status == 200:
                                        content_type = response.content_type
                                        if "json" in content_type:
                                            data = await response.json()
                                        else:
                                            data = await response.text()
                                            data = json.loads(data)
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
                            print(f"定義エラー2：{e}")

                        # descriptionを初期化する
                        description = ""

                        # 情報を定義する
                        url = f'http://{IP}/players.json'
                        try:
                            async with aiohttp.ClientSession() as session:
                                async with session.get(url) as response:
                                    if await response.text() != "[]":
                                        data1 = await response.text()
                                        data2 = data1.replace('""', '')
                                        data = json.loads(data2)
                                        print(data)
                                        for item in data:
                                            name = item["name"]
                                            id = item["id"]
                                            ping = item["ping"]
                                            discord_id = [identifier.split(":")[1] for identifier in item["identifiers"] if identifier.startswith("discord")]
                                            if discord_id:
                                                user_id = f'{discord_id[0]}'
                                                user = await self.bot.fetch_user(user_id)
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
                            print(f"定義エラー3：{e}")
                        print(player_count)
                        print(max_player)

                        try:
                            if status_data['work'] == "true":
                                embed = discord.Embed(title='Server Status',color=discord.Colour.yellow())
                                embed.add_field(name='Status', value=server_status,inline=False)
                                embed.set_author(name=guild.name,icon_url=guild.icon.url)
                                embed.timestamp = datetime.now()
                                await message.edit(embed=embed)
                            else:
                                embed = discord.Embed(title='Server Status',description=description,color=color)
                                embed.add_field(name='Player', value=f'```[{player_count}/{max_player}]```',inline=False)
                                embed.add_field(name='Status', value=server_status,inline=False)
                                embed.set_author(name=guild.name,icon_url=guild.icon.url)
                                embed.set_footer(text=f"connect {IP}")
                                embed.timestamp = datetime.now()
                                await message.edit(embed=embed)
                            print("embedを更新しました")
                        except discord.HTTPException as e:
                            print(f"メッセージの取得に失敗しました: {e}")
                        if status_data["work"] == "true":
                            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"作業中"),status=discord.Status.dnd)
                            print("ステータスを更新しました")
                            await asyncio.sleep(10)
                            await self.bot.change_presence(activity=discord.Activity( type=discord.ActivityType.playing, name=patch),status=discord.Status.dnd,)
                            await asyncio.sleep(5)
                        else:
                            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"[{player_count}/{max_player}]がサーバー"),status=discord.Status.online)
                            print("ステータスを更新しました")
                            await asyncio.sleep(10)
                            await self.bot.change_presence(activity=discord.Activity( type=discord.ActivityType.playing, name=patch),status=discord.Status.online,)
                            await asyncio.sleep(5)
                except Exception as e:
                    if status_data["work"] == "true":
                        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"作業中"),status=discord.Status.dnd)
                        print("ステータスを更新しました")
                        await asyncio.sleep(10)
                        await self.bot.change_presence(activity=discord.Activity( type=discord.ActivityType.playing, name=patch),status=discord.Status.dnd,)
                        await asyncio.sleep(5)
                    else:
                        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"オフライン"),status=discord.Status.idle)
                        print("ステータスをオフラインに更新しました")
                    print(f"エラー：{e}")
                    await asyncio.sleep(10)
                    await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=patch),status=discord.Status.idle)
                    await asyncio.sleep(5)
        else:
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="メンテナンス"),status=discord.Status.dnd)
