import asyncio
import disnake
from disnake.ext import commands, tasks
import random
import json
from collections import OrderedDict
import time
from itertools import cycle
from korcen import korcen
import re
from PIL import ImageFont, ImageDraw, Image
import requests
import os
import io
from datetime import datetime

intents = disnake.Intents().all()
bot = commands.Bot(intents=intents)


@bot.event
async def on_ready():
    print(f"[!] 다음으로 로그인에 성공했습니다.")
    print(f"[!] 다음 : {bot.user.name}")
    print(f"[!] 다음 : {bot.user.id}")

    os.system(f'title {bot.user.name} - {bot.user.id}') 

    change_status.start()
    check_voice.start()
    check_activity.start()


status = cycle(["나만의 작은 상점"])


def hex_to_rgb(hex):
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
    

@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=disnake.Game(next(status)))


@tasks.loop(seconds=60)
async def check_voice():
    for guild in bot.guilds:
        try:
            with open(f'guild/{guild.id}.json', encoding="utf-8") as f:
                json_object = json.load(f)
            for channel in guild.voice_channels:
                for member in channel.members:
                    if member.bot:
                        None
                    else:
                        try:
                            with open(f'guild/{guild.id}.json', encoding="utf-8") as f:
                                json_object = json.load(f)
                                try:
                                    json_object['user'][str(member.id)]["money"] += json_object['setting']['voice']
                                    json_object['user'][str(member.id)]["voice"] += 1
                                except:
                                        json_object['user'][str(member.id)] = {}
                                        json_object['user'][str(member.id)]["money"] = 0
                                        json_object['user'][str(member.id)]["chat"] = 0
                                        json_object['user'][str(member.id)]["voice"] = 0
                                        json_object['user'][str(member.id)]["attendance"] = 0
                                        json_object['user'][str(member.id)]["activity"] = 0
                                        json_object['user'][str(member.id)]["day"] = 0
                            with open(f'guild/{guild.id}.json', 'w', encoding="utf-8") as f:
                                json.dump(json_object, f, indent=2, ensure_ascii=False)
                        except:
                            pass
        except:
            pass
        


@tasks.loop(hours=1)
async def check_activity():
    for guild in bot.guilds:
        try:
            with open(f'guild/{guild.id}.json', encoding="utf-8") as f:
                json_object = json.load(f)
            for user in guild.members: 
                user_activities = None
                if user.bot:
                    pass
                else:
                    try: 
                        if user.activities[1].type.name == "playing": 
                            user_activities = user.activities[1].name 
                    except: 
                        try: 
                            if user.activities[0].type.name == "playing": 
                                user_activities = user.activities[0].name 
                        except: 
                            pass
                    if user_activities != None:
                        user_activities.lower()
                        ic = 0
                        if "lost ark" in user_activities:
                            ic = 1
                            user_activities = "Lost Ark"
                        elif "roblox" in user_activities:
                            ic = 1
                            user_activities = "Roblox"
                        elif "apex legends" in user_activities:
                            ic = 1
                            user_activities = "Apex Legends"
                        elif "battlegrounds" in user_activities:
                            ic = 1
                            user_activities = "BATTLEGROUNDS"
                        elif "valorant" in user_activities:
                            ic = 1
                            user_activities = "VALORANT"
                        elif "league of legends" in user_activities:
                            ic = 1
                            user_activities = "League of Legends"
                        elif "genshin impact" in user_activities:
                            ic = 1
                            user_activities = "Genshin Impact"
                        elif "minecraft" in user_activities:
                            ic = 1
                            user_activities = "Minecraft"
                        elif "overwatch" in user_activities:
                            ic = 1
                            user_activities = "Overwatch"
                        elif "maplestory" in user_activities:
                            ic = 1
                            user_activities = "MapleStory"
                        elif "grand theft auto" in user_activities or"gta" in user_activities:
                            ic = 1
                            user_activities = "Grand Theft Auto"
                        elif "Fire and Ice" in user_activities:
                            ic = 1
                            user_activities = "A Dance of Fire and Ice"
                        elif "fall flat" in user_activities:
                            ic = 1
                            user_activities = "Human: Fall Flat"
                        elif "cities: skylines" in user_activities:
                            ic = 1
                            user_activities = "Cities: Skylines"
                        elif "tom clancy's rainbow six siege" in user_activities:
                            ic = 1
                            user_activities = "Tom Clancy's Rainbow Six Siege"
                        elif "goose goose duck" in user_activities:
                            ic = 1
                            user_activities = "Goose Goose Duck"
                        try:
                            with open(f'guild/{guild.id}.json', encoding="utf-8") as f:
                                json_object = json.load(f)
                                activity = json_object['setting']['activity'][str(user_activities)]
                        except:
                            if ic == 1:
                                json_object['setting']['activity'][str(user_activities)] = 0
                        try:
                            json_object['user'][str(user.id)]["money"] += activity
                            if ic == 1:
                              json_object['user'][str(user.id)]["activity"] += 1
                        except:
                            try:
                                json_object['user'][str(user.id)]["money"] += activity
                            except:
                                    json_object['user'][str(user.id)] = {}
                                    json_object['user'][str(user.id)]["money"] = 0
                                    json_object['user'][str(user.id)]["chat"] = 0
                                    json_object['user'][str(user.id)]["voice"] = 0
                                    json_object['user'][str(user.id)]["attendance"] = 0
                                    json_object['user'][str(user.id)]["activity"] = 0
                                    json_object['user'][str(user.id)]["day"] = 0
                        with open(f'guild/{guild.id}.json', 'w', encoding="utf-8") as f:
                                json.dump(json_object, f, indent=2, ensure_ascii=False)
        except:
            pass
        


@bot.event
async def on_guild_join(guild):
    await bot.get_channel(int(938656148423344178)).send(f'새로운 서버에 추가되었습니다. (**현재 서버수 : {len(bot.guilds)}**)')
    

def uid(guild = int, user = int):
    return str(guild.id*10000000000000000000+user.id)


MAX_SIZE_COOLDOWN = 128 # 쿨타임 저장
cache_cooldown = OrderedDict()  
MAX_SIZE_guild = 128 # 쿨타임 저장
cache_guild = OrderedDict()  

def fetch_cooldown(uid):
    try:  # 캐시에서 마지막 채팅 시간
        chat_cooldown = cache_cooldown[uid]
    except:  # 없으면 현재 시간
        chat_cooldown = time.time()
    return chat_cooldown

def chat_cooldown(message):
    uid = message.author.id
    if uid in cache_cooldown:
        cache_cooldown.move_to_end(uid)  # 가장 최근에 사용된 아이템은 캐쉬의 맨 뒤로 이동
        try:
            with open(f'guild/{message.guild.id}.json', encoding="utf-8") as f:
                json_object = json.load(f)
                try:
                    json_object['user'][str(message.author.id)]["money"] += json_object['setting']['chat']
                except:
                        json_object['user'][str(message.author.id)] = {}
                        json_object['user'][str(message.author.id)]["money"] = 0
                        json_object['user'][str(message.author.id)]["chat"] = 0
                        json_object['user'][str(message.author.id)]["voice"] = 0
                        json_object['user'][str(message.author.id)]["attendance"] = 0
                        json_object['user'][str(message.author.id)]["activity"] = 0
                        json_object['user'][str(message.author.id)]["day"] = 0
            with open(f'guild/{message.guild.id}.json', 'w', encoding="utf-8") as f:
                json.dump(json_object, f, indent=2, ensure_ascii=False)
        except:
            pass

    if len(cache_cooldown) == MAX_SIZE_COOLDOWN:
        cache_cooldown.popitem(last=False)  # 캐시 용량이 꽉 찾을 때는 캐쉬에 맨 앞에 있는 아이템 삭제

    cache_cooldown[uid] = fetch_cooldown(uid)
    return cache_cooldown[uid]


@bot.event
async def on_message(message):
    if message.author.bot:
        return  # 봇이면 작동X
    lastTime = int(chat_cooldown(message))
    late_time = int(time.time())-lastTime  # 지연시간
    if korcen.check(message.content):
        return
    if late_time >= 2:  # 2초 이상
        cache_cooldown.move_to_end(message.author.id)  # 끝으로 이동
        cache_cooldown.popitem(last=True)
        chat_cooldown(message)
        try:
            with open(f'guild/{message.guild.id}.json', encoding="utf-8") as f:
                json_object = json.load(f)
                try:
                    json_object['user'][str(message.author.id)]["money"] += json_object['setting']['chat']
                    json_object['user'][str(message.author.id)]["chat"] += 1
                except:
                        json_object['user'][str(message.author.id)] = {}
                        json_object['user'][str(message.author.id)]["money"] = 0
                        json_object['user'][str(message.author.id)]["chat"] = 0
                        json_object['user'][str(message.author.id)]["voice"] = 0
                        json_object['user'][str(message.author.id)]["attendance"] = 0
                        json_object['user'][str(message.author.id)]["activity"] = 0
                        json_object['user'][str(message.author.id)]["day"] = 0
            with open(f'guild/{message.guild.id}.json', 'w', encoding="utf-8") as f:
                json.dump(json_object, f, indent=2, ensure_ascii=False, sort_keys=True)
        except:
            pass


@bot.slash_command(name="도움말", description="봇의 사용법을 알려주는 링크를 보냅니다.")
async def help(inter: disnake.ApplicationCommandInteraction):
    await inter.response.defer()
    await inter.followup.send("https://tanat.gitbook.io/distore/", file=disnake.File("DISTORE.gif"))


@bot.slash_command(name="이용")
@commands.default_member_permissions(administrator=True)
async def use(inter):
    pass


@use.sub_command(name="동의", description="자세한 내용은 도움에서 확인하세요.")
async def append(inter: disnake.ApplicationCommandInteraction):
    await inter.response.defer()
    try:
        with open(f'guild/{inter.guild.id}.json', encoding="utf-8") as f:
            json_object = json.load(f)
    except:
        json_object = {
            "setting":{
                "chat": 0,
                "voice": 0,
                "attendance": 0,
                "moneyName": "원",
                "logChannel": 0,
                "embed_color": "",
                "game1": 0,
                "game2": 0,
                "game3": 0,
                "game4": 0,
                "game5": 0,
                "game6": 0,
                "game7": 0,
                "game8": 0,
                "game9": 0,
                "game10": 0,
                "game11": 0,
                "game12": 0,
                "game13": 0,
                "game14": 0,
                "game15": 0,
                "game16": 0,
                "game17": 0,
                "game18": 0,
                "game19": 0,
                "game20": 0,
                "activity": {
                    "Lost Ark": 0,
                    "Roblox": 0,
                    "Apex Legends": 0,
                    "BATTLEGROUNDS": 0,
                    "VALORANT": 0,
                    "League of Legends": 0,
                    "Genshin Impact": 0,
                    "Minecraft": 0,
                    "Overwatch": 0,
                    "MapleStory": 0,
                    "Grand Theft Auto":0,
                    "A Dance of Fire and Ice": 0,
                    "Human: Fall Flat": 0,
                    "Cities: Skylines":0,
                    "VRChat": 0,
                    "SuddenAttack": 0
                }
            },
            "user": {
            },
            "goods": {
            },
            "custom":{
                "package": "",
                "color1": "",
                "color2": "",
                "color3": "",
                "color4": "",
                "color5": "",
                "color6": "",
                "color7": "",
                "color8": "",
                "color9": "",
                "color10": "",
                "color11": "",
                "color12": "",
                "color13": "",
                "color14": "",
                "color15": "",
                "color16": "",
                "color17": "",
                "color18": "",
                "color19": "",
                "color20": "",
                "color21": "",
                "color22": "",
                "color23": "",
                "color24": "",
                "color25": "",
                "color26": "",
                "color27": "",
                "color28": "",
                "color29": "",
                "color30": "",
                "color31": "",
                "color32": "",
                "color33": "",
                "color34": "",
                "color35": "",
                "color36": "",
                "color37": "",
                "color38": "",
                "color39": "",
                "color40": "",
            },
            "premium":{
                "expiration_date": 0,
                "package": {}
            }
        }

        with open(f'guild/{inter.guild.id}.json', 'w', encoding="utf-8") as f:
            json.dump(json_object, f, indent=2, ensure_ascii=False)
        embed = disnake.Embed(
            title=f"DISTORE이용에 동의하셨습니다.", description=f"지금부터 서버의 활동을 기록합니다.\n", color=0xFFB9B9)
    else:
        embed = disnake.Embed(
            title=f"이미 DISTORE이용에 동의하셨습니다.", description=f"이미 동의한 서버입니다.\n자세한 내용은 [동의 내용]()을 참고하세요. ", color=0xFFB9B9)
    await inter.followup.send(embed=embed)


@bot.slash_command(name="설정")
@commands.default_member_permissions(administrator=True)
async def set(inter):
    pass


@set.sub_command(name="채팅", description="체팅을 통해 얻는 금액을 설정합니다.")
async def set_chat(inter: disnake.ApplicationCommandInteraction, 값:commands.Range[0, 10000]):
    await inter.response.defer()
    try:
        with open(f'guild/{inter.guild.id}.json', encoding="utf-8") as f:
            json_object = json.load(f)
            json_object['setting']['chat'] = 값
            moneyName = json_object['setting']['moneyName']
        with open(f'guild/{inter.guild.id}.json', 'w', encoding="utf-8") as f:
            json.dump(json_object, f, indent=2, ensure_ascii=False)
    except:
        embed = disnake.Embed(
        title=f"오류 발생", description=f"데이터를 저장하는 과정에서 오류가 발생하였습니다.\n오류가 계속 될 경우 문의를 해주시기 바랍니다.", color=0xFFB9B9)
        await inter.followup.send(embed=embed)
        return
    embed = disnake.Embed(
        title=f"설정 완료!", description=f"이제부터 채팅을 칠때마다 `{값}`{moneyName}을 받습니다.\n도배를 방지하기 위해 2초에 1회로 제한합니다.", color=0xFFB9B9)
    await inter.followup.send(embed=embed)


@set.sub_command(name="음성채팅", description="음성채팅으로 얻는 금액을 설정합니다.")
async def set_voice(inter: disnake.ApplicationCommandInteraction, 값:commands.Range[0, 100000]):
    await inter.response.defer()
    try:
        with open(f'guild/{inter.guild.id}.json', encoding="utf-8") as f:
            json_object = json.load(f)
            json_object['setting']['voice'] = 값
            moneyName = json_object['setting']['moneyName']
        with open(f'guild/{inter.guild.id}.json', 'w', encoding="utf-8") as f:
            json.dump(json_object, f, indent=2)
    except:
        embed = disnake.Embed(
        title=f"오류 발생", description=f"데이터를 저장하는 과정에서 오류가 발생하였습니다.\n오류가 계속 될 경우 문의를 해주시기 바랍니다.", color=0xFFB9B9)
        await inter.followup.send(embed=embed)
        return
    embed = disnake.Embed(
        title=f"설정 완료!", description=f"음성채널에 접속하여 있다면 1분마다 `{값}`{moneyName}을 받습니다.", color=0xFFB9B9)
    await inter.followup.send(embed=embed)


@set.sub_command(name="출석", description="출석을 통해 얻는 금액을 설정합니다.")
async def set_attendance(inter: disnake.ApplicationCommandInteraction, 값:commands.Range[0, 10000000]):
    await inter.response.defer()
    try:
        with open(f'guild/{inter.guild.id}.json', encoding="utf-8") as f:
            json_object = json.load(f)
            json_object['setting']['attendance'] = 값
            moneyName = json_object['setting']['moneyName']
        with open(f'guild/{inter.guild.id}.json', 'w', encoding="utf-8") as f:
            json.dump(json_object, f, indent=2, ensure_ascii=False)
    except:
        embed = disnake.Embed(
        title=f"오류 발생", description=f"데이터를 저장하는 과정에서 오류가 발생하였습니다.\n오류가 계속 될 경우 문의를 해주시기 바랍니다.", color=0xFFB9B9)
        await inter.followup.send(embed=embed)
        return
    embed = disnake.Embed(
        title=f"설정 완료!", description=f"하루에 한번 출석을 할때 `{값}`{moneyName}을 받습니다.", color=0xFFB9B9)
    await inter.followup.send(embed=embed)


activities = commands.option_enum({"리그 오브 레전드": "League of Legends", "오버워치": "Overwatch", "배틀그라운드": "BATTLEGROUNDS", "발로란트": "VALORANT", "마인크래프트": "Minecraft", "로스트아크": "Lost Ark", "로블록스": "Roblox", "원신": "Genshin Impact", "메이플스토리": "MapleStory", "GTA": "Grand Theft Auto", "얼불춤": "A Dance of Fire and Ice", "Human: Fall Flat": "Human: Fall Flat", "시티즈 스카이라인": "Cities: Skylines", "레인 보우 식스 시즈": "Tom Clancy's Rainbow Six Siege", "구스구스덕": "Goose Goose Duck"})

@set.sub_command(name="활동", description="활동을 통해 얻는 금액을 설정합니다.")
async def set_activity(inter: disnake.ApplicationCommandInteraction, 활동:activities, 값:commands.Range[0, 100000]):
    await inter.response.defer()
    try:
        with open(f'guild/{inter.guild.id}.json', encoding="utf-8") as f:
            json_object = json.load(f)
            json_object['setting']['activity'][활동] = 값
            moneyName = json_object['setting']['moneyName']
        with open(f'guild/{inter.guild.id}.json', 'w', encoding="utf-8") as f:
            json.dump(json_object, f, indent=2, ensure_ascii=False)
    except:
        embed = disnake.Embed(
        title=f"오류 발생", description=f"데이터를 저장하는 과정에서 오류가 발생하였습니다.\n오류가 계속 될 경우 문의를 해주시기 바랍니다.", color=0xFFB9B9)
        await inter.followup.send(embed=embed)
        return
    embed = disnake.Embed(
        title=f"설정 완료!", description=f"`{활동}`을 하고있다면 1시간마다 `{값}`{moneyName}을 받습니다.", color=0xFFB9B9)
    await inter.followup.send(embed=embed)


@set.sub_command(name="로그채널", description="DISTORE의 로그를 보낼 채널을 설정합니다.")
async def set_logChannel(inter: disnake.ApplicationCommandInteraction, 채널:disnake.TextChannel):
    await inter.response.defer()
    try:
        with open(f'guild/{inter.guild.id}.json', encoding="utf-8") as f:
            json_object = json.load(f)
            json_object['setting']['logChannel'] = 채널.id
            moneyName = json_object['setting']['moneyName']
        with open(f'guild/{inter.guild.id}.json', 'w', encoding="utf-8") as f:
            json.dump(json_object, f, indent=2, ensure_ascii=False)
    except:
        embed = disnake.Embed(
        title=f"오류 발생", description=f"데이터를 저장하는 과정에서 오류가 발생하였습니다.\n오류가 계속 될 경우 문의를 해주시기 바랍니다.", color=0xFFB9B9)
        await inter.followup.send(embed=embed)
        return
    embed = disnake.Embed(
        title=f"설정 완료!", description=f"로그 채널을 {채널.mention}으로 설정했습니다.\n구매 로그가 해당 채널로 전송됩니다.", color=0xFFB9B9)
    await inter.followup.send(embed=embed)


@set.sub_command(name="화폐단위", description="화폐단위를 설정합니다.")
async def set_moneyName(inter: disnake.ApplicationCommandInteraction, 단위: commands.String[1, 7]):
    await inter.response.defer()
    try:
        with open(f'guild/{inter.guild.id}.json', encoding="utf-8") as f:
            json_object = json.load(f)
            json_object['setting']['moneyName'] = 단위
        with open(f'guild/{inter.guild.id}.json', 'w', encoding="utf-8") as f:
            json.dump(json_object, f, indent=2, ensure_ascii=False)
    except:
        embed = disnake.Embed(
        title=f"오류 발생", description=f"데이터를 저장하는 과정에서 오류가 발생하였습니다.\n오류가 계속 될 경우 문의를 해주시기 바랍니다.", color=0xFFB9B9)
        await inter.followup.send(embed=embed)
        return
    embed = disnake.Embed(
        title=f"설정 완료!", description=f"화폐 단위를 {단위}로 설정하였습니다.", color=0xFFB9B9)
    await inter.followup.send(embed=embed)


page = commands.option_enum(["상품 목록 이미지", "유저 정보 이미지", "구매 확인서 이미지", "임베드 색", "상품 목록 제목 색", "상품 목록 상품이름 색", "상목 목록 상품설명 색", "상품 목록 가격 색", "상품 정보 재고 색"])

@set.sub_command(name="꾸미기", description="봇이 보내는 이미지 또는 임베드의 색을 변경합니다.")
async def set_image(inter: disnake.ApplicationCommandInteraction, 항목: page, 값: commands.String[1, 500]):
    await inter.response.defer()
    try:
        with open(f'guild/{inter.guild.id}.json', encoding="utf-8") as f:
            json_object = json.load(f)
    except:
        embed = disnake.Embed(
        title=f"사용 불가", description=f"해당 서버는 이용 동의를 하지 않았습니다.\n동의를 완료한 서버에서 해당 메세지가 계속 나올 경우 문의를 해주시기 바랍니다.", color=0xFFB9B9)
        await inter.followup.send(embed=embed)
        return
    if 값 == "제거" or 값 == "삭제":
        값 = ""
    if "이미지" in 항목:
        if 값[0:4] != "http" and 값 != "":
            embed = disnake.Embed(
            title=f"잘못된 값입니다.", description=f"이미지의 경우 이미지url를 입력해 주시기 바랍니다.", color=0xFFB9B9)
            await inter.followup.send(embed=embed)
            return
        elif 값 == "":
            if "목록" in 항목:
                항목 = "목록"
            if "유저" in 항목:
                항목 = "유저"
            if "구매" in 항목:
                항목 = "구매"
            os.remove(f"custom/{항목}{inter.guild.id}.png")
            embed = disnake.Embed(
                title=f"삭제 완료", description=f"{항목}의 이미지를 삭제하고 기본이미지로 설정하였습니다.", color=0xFFB9B9)
            await inter.followup.send(embed=embed)
            return
        else:
            try:
                if "목록" in 항목:
                    항목 = "목록"
                if "유저" in 항목:
                    항목 = "유저"
                if "구매" in 항목:
                    항목 = "구매"
                result = requests.get(값)
                with open(f"custom/{항목}{inter.guild.id}.png", "wb") as fp:
                    fp.write(result.content)
            except:
                embed = disnake.Embed(
                    title=f"오류 발생", description=f"이미지를 저장하는 중에 오류가 발생하였습니다.\n이미지의 url이 올바르게 입력했는지 확인 해 주시고 오류가 계속 될 경우 문의를 해주시기 바랍니다.", color=0xFFB9B9)
                await inter.followup.send(embed=embed)
                return
            embed = disnake.Embed(
                title=f"저장 완료", description=f"이미지를 저장하였습니다.\n이미지의 비율이나 해상도가 안 맞을 시 제대로 출력이 되지 않을 수 있습니다.\n[권장 사이즈 안내](https://tanat.gitbook.io/distore/admin/undefined-2/undefined/deco)\n\n기본 이미지로 변경하시려면 `값`에 `삭제` 또는 `제거`를 입력해 주세요.", color=0xFFB9B9)
            await inter.followup.send(embed=embed)
    elif "색" in 항목:
        값 = re.sub("#", "", 값)
        if len(값) != 6:
            embed = disnake.Embed(
            title=f"잘못된 값입니다.", description=f"색의 경우 헥스 코드를 입력해 주시기 바랍니다.\n네이버에 색상 팔레트를 입력해 원하는 색상의 코드를 알아보세요\n**예시**\n```빨강: #FF0000\n주황: #FF5E00\n노랑: #FFE400\n초록: #1DDB16\n하늘: #48FFFF\n파랑: #0054FF\n보라: #5F00FF```", color=0xFFB9B9)
            await inter.followup.send(embed=embed)
            return
        if "임베드" in 항목:
            항목 = "color1"
        if "목록 제목" in 항목:
            항목 = "color2"
        if "목록 이름" in 항목:
            항목 = "color3"
        if "목록 설명" in 항목:
            항목 = "color4"
        if "목록 가격" in 항목:
            항목 = "color5"
        if "목록 재고" in 항목:
            항목 = "color6"
        
        try:
            with open(f'guild/{inter.guild.id}.json', encoding="utf-8") as f:
                json_object = json.load(f)
                json_object["custom"][항목] = 값
            with open(f'guild/{inter.guild.id}.json', 'w', encoding="utf-8") as f:
                json.dump(json_object, f, indent=2, ensure_ascii=False)
        except:
            embed = disnake.Embed(
            title=f"오류 발생", description=f"데이터를 저장하는 과정에서 오류가 발생하였습니다.\n오류가 계속 될 경우 문의를 해주시기 바랍니다.", color=0xFFB9B9)
            await inter.followup.send(embed=embed)
            return
        embed = disnake.Embed(
            title=f"저장 완료", description=f"{항목}의 색을 지정하였습니다.\n기본 색상으로 변경하시려면 `값`에 `삭제` 또는 `제거`를 입력해 주세요.", color=0xFFB9B9)
        await inter.followup.send(embed=embed)
        
    else:
        embed = disnake.Embed(
        title=f"오류 발생", description=f"항목이 잘못 되었습니다.\n오류가 계속 될 경우 문의를 해주시기 바랍니다.", color=0xFFB9B9)
        await inter.followup.send(embed=embed)
        return


package = commands.option_enum(["패키지가 존재하지 않습니다"])

@set.sub_command(name="패키지", description="디자인 패키지를 설정합니다")
async def set_image(inter: disnake.ApplicationCommandInteraction, 패키지: package):
    await inter.response.defer()

@bot.slash_command(name="서버")
async def server(inter):
    pass

@server.sub_command(name="정보", description="현재 서버의 정보를 보여줍니다")
async def sets(inter):
    await inter.response.defer()
    try:
        with open(f'guild/{inter.guild.id}.json', encoding="utf-8") as f:
            json_object = json.load(f)
    except:
        embed = disnake.Embed(
        title=f"사용 불가", description=f"해당 서버는 이용 동의를 하지 않았습니다.\n동의를 완료한 서버에서 해당 메세지가 계속 나올 경우 문의를 해주시기 바랍니다.", color=0xFFB9B9)
        await inter.followup.send(embed=embed)
        return
    try:
        with open(f'guild/{inter.guild.id}.json', encoding="utf-8") as f:
            json_object = json.load(f)
            chat = json_object["setting"]["chat"]
            voice = json_object["setting"]["voice"]
            attendance = json_object["setting"]["attendance"]
            activity = json_object["setting"]["activity"]
            moneyName = json_object["setting"]["moneyName"]
            logChannel = json_object["setting"]["logChannel"]
            embed_color = json_object["setting"]["embed_color"]
            user = json_object["user"]
            goods = json_object["goods"]

    except:
        embed = disnake.Embed(
        title=f"오류 발생", description=f"데이터를 불러오는 과정에서 오류가 발생하였습니다.\n오류가 계속 될 경우 문의를 해주시기 바랍니다.\n오류코드:서버정보1", color=0xFFB9B9)
        await inter.followup.send(embed=embed)
        return
    embed = disnake.Embed(
        title=f"{inter.guild}의 정보", description="", color=0xFFB9B9)
    embed.add_field(name="돈", value=f"채팅: `{chat}`\n음성채팅: `{voice}`\n출석: `{attendance}`\n활동:\n```json\n{activity}\n```", inline=False)
    embed.add_field(name="기타", value=f"화폐단위: `{moneyName}`\n로그채널: <#{logChannel}>\n임베드 색상: `{embed_color}`", inline=False)
    embed.add_field(name="DB", value=f"유저수: `{len(user)}`\n상품수: `{len(goods)}`", inline=False)
    await inter.followup.send(embed=embed)


def get_round(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    return alpha


@bot.user_command(name="유저 정보")
async def help(inter: disnake.ApplicationCommandInteraction):
    await inter.response.defer()
    if inter.target.bot:
        embed = disnake.Embed(
            title=f"봇에게는 사용이 불가합니다.", description=f"", color=0xFFB9B9)
        await inter.followup.send.send(embed=embed)
        return
    try:
        with open(f'guild/{inter.guild.id}.json', encoding="utf-8") as f:
            json_object = json.load(f)
    except:
        embed = disnake.Embed(
            title=f"사용 불가", description=f"해당 서버는 이용 동의를 하지 않았습니다.\n동의를 완료한 서버에서 해당 메세지가 계속 나올 경우 문의를 해주시기 바랍니다.", color=0xFFB9B9)
        await inter.followup.send(embed=embed)
        return
    try:
        with open(f'guild/{inter.guild.id}.json', encoding="utf-8") as f:
            json_object = json.load(f)
            try:
                money = json_object['user'][str(inter.target.id)]["money"]
            except:
                money = 0
            try:
                chat = json_object['user'][str(inter.target.id)]["chat"]
            except:
                chat = 0
            try:
                voice = json_object['user'][str(inter.target.id)]["voice"]
            except:
                voice = 0
            try:
                attendance = json_object['user'][str(inter.target.id)]["attendance"]
            except:
                attendance = 0
            try:
                activity = json_object['user'][str(inter.target.id)]["activity"]
            except:
                activity = 0
            try:
                moneyName = json_object['setting']['moneyName']
            except:
                moneyName = "원"
            try:
                package = json_object['custom']['package']
                name_color = json_object["custom"]["color7"]
                money_color = json_object["custom"]["color8"]
                info_color = json_object["custom"]["color9"]
            except:
                embed = disnake.Embed(
                title=f"오류 발생", description=f"커스텀 데이터을 불러오는 과정에서 오류가 발생하였습니다.\n오류가 계속 될 경우 문의를 해주시기 바랍니다.\n오류 코드: 내정보1", color=0xFFB9B9)
                await inter.followup.send(embed=embed)
                return
    except:
        embed = disnake.Embed(
            title=f"오류 발생", description=f"데이터를 불러오는 과정에서 오류가 발생하였습니다.\n오류가 계속 될 경우 문의를 해주시기 바랍니다.\n오류 코드: 내정보2", color=0xFFB9B9)
        await inter.followup.send(embed=embed)
        return
    if moneyName == None:
        moneyName = "원"

    if package != "": #패키지
        try:
            with open(f'package/{package}.json', encoding="utf-8") as f:
                json_object = json.load(f)
                try:
                    avater_location = json_object["user_info"]["location1"]
                    avater_position = json_object["user_info"]["location1_position"]
                    avater_size = json_object["user_info"]["font_size1"]
                    name_location = json_object["user_info"]["location2"]
                    name_position = json_object["user_info"]["location2_position"]
                    money_location = json_object["user_info"]["location3"]
                    money_position = json_object["user_info"]["location3_position"]
                    chat_location = json_object["user_info"]["location4"]
                    chat_position = json_object["user_info"]["location4_position"]
                    voice_location = json_object["user_info"]["location5"]
                    voice_position = json_object["user_info"]["location5_position"]
                    attendance_location = json_object["user_info"]["location6"]
                    attendance_position = json_object["user_info"]["location6_position"]
                    activity_location = json_object["user_info"]["location7"]
                    activity_position = json_object["user_info"]["location7_position"]
                except:
                    embed = disnake.Embed(
                    title=f"오류 발생", description=f"글자의 위치를 불러오는데 오류가 발생하였습니다.\n문의해 주시기 바랍니다.\n오류 코드: 내정보3", color=0xFFB9B9)
                    await inter.followup.send(embed=embed)
                    return
                try:
                    name_font = json_object["user_info"]["font2"] #name
                    name_font_size = json_object["user_info"]["font_size2"]
                    name_color = json_object["user_info"]["color2"]
                    money_font = json_object["user_info"]["font3"] #money
                    money_font_size = json_object["user_info"]["font_size3"]
                    money_color = json_object["user_info"]["color3"]
                    info_font = json_object["user_info"]["font4"] #chat,voice,attendance,activity
                    info_font_size = json_object["user_info"]["font_size4"]
                    info_color = json_object["user_info"]["color4"]
                except:
                    embed = disnake.Embed(
                    title=f"오류 발생", description=f"글자의 폰트와 색상을 불러오는데 오류가 발생하였습니다.\n문의해 주시기 바랍니다.\n오류 코드: 내정보4", color=0xFFB9B9)
                    await inter.followup.send(embed=embed)
                    return
        except:
            embed = disnake.Embed(
            title=f"오류 발생", description=f"패키지 형식을 불러오는데 오류가 발생하였습니다.\n문의해 주시기 바랍니다.\n오류 코드: 내정보5", color=0xFFB9B9)
            await inter.followup.send(embed=embed)
            return

        try:
            img = Image.open(f"package/유저{package}.png")
            W, H = (img.width, img.height)
        except:
            embed = disnake.Embed(
                title=f"오류 발생", description=f"패키지의 이미지를 불러오지 못했습니다.\n오류가 계속 될 경우 문의해 주세요.\n오류 코드: 내정보6", color=0xFFB9B9)
            await inter.followup.send(embed=embed)
            return
    else: #기본&커스텀
        try:
            with open('package/nomal.json', encoding="utf-8") as f:
                json_object = json.load(f)
                try:
                    avater_location = json_object["user_info"]["location1"]
                    avater_position = json_object["user_info"]["location1_position"]
                    avater_size = json_object["user_info"]["font_size1"]
                    name_location = json_object["user_info"]["location2"]
                    name_position = json_object["user_info"]["location2_position"]
                    money_location = json_object["user_info"]["location3"]
                    money_position = json_object["user_info"]["location3_position"]
                    chat_location = json_object["user_info"]["location4"]
                    chat_position = json_object["user_info"]["location4_position"]
                    voice_location = json_object["user_info"]["location5"]
                    voice_position = json_object["user_info"]["location5_position"]
                    attendance_location = json_object["user_info"]["location6"]
                    attendance_position = json_object["user_info"]["location6_position"]
                    activity_location = json_object["user_info"]["location7"]
                    activity_position = json_object["user_info"]["location7_position"]
                except:
                    embed = disnake.Embed(
                    title=f"오류 발생", description=f"글자의 위치를 불러오는데 오류가 발생하였습니다.\n문의해 주시기 바랍니다.\n오류 코드: 내정보7", color=0xFFB9B9)
                    await inter.followup.send(embed=embed)
                    return
                try:
                    name_font = json_object["user_info"]["font2"] #name
                    name_font_size = json_object["user_info"]["font_size2"]
                    if name_color == "":
                        name_color = json_object["user_info"]["color2"]
                    money_font = json_object["user_info"]["font3"] #money
                    money_font_size = json_object["user_info"]["font_size3"]
                    if money_color == "":
                        money_color = json_object["user_info"]["color3"]
                    info_font = json_object["user_info"]["font4"] #chat,voice,attendance,activity
                    info_font_size = json_object["user_info"]["font_size4"]
                    if info_color == "":
                        info_color = json_object["user_info"]["color4"]
                except:
                    embed = disnake.Embed(
                    title=f"오류 발생", description=f"글자의 폰트와 색상을 불러오는데 오류가 발생하였습니다.\n문의해 주시기 바랍니다.\n오류 코드: 내정보8", color=0xFFB9B9)
                    await inter.followup.send(embed=embed)
                    return

        except:
            embed = disnake.Embed(
                title=f"오류 발생", description=f"기본 형식을 불러오는데 오류가 발생하였습니다.\n문의해 주시기 바랍니다.\n오류 코드: 내정보9", color=0xFFB9B9)
            await inter.followup.send(embed=embed)
            return

        try:
            img = Image.open(f"custom/유저{inter.guild.id}.png")
        except:
            img = Image.open("DISTORE_user.png")

        W, H = (img.width, img.height)

        if package == "":
            WR = W/3200
            HR = H/1800
            print("유저배율:" + str(WR) + "," + str(HR))
            name_len = len(inter.target.name+"#"+inter.target.discriminator) 
            font_name = ImageFont.truetype(name_font, int(name_font_size*WR+15-name_len*1.7))
            font_money = ImageFont.truetype(money_font, int(money_font_size*WR))
            font_info = ImageFont.truetype(info_font, int(info_font_size*WR))
        else:
            WR = 1

    #avater
    base = Image.new('RGBA',size=(W,H))

    base.paste(img, (0,0))

    w = avater_size*WR

    try:
        try:
            avatar = Image.open(io.BytesIO(requests.get(inter.target.avatar).content)).resize((int(avater_size*WR), int(avater_size*HR)))
        except:
            avatar = Image.open(io.BytesIO(requests.get(inter.target.default_avatar).content)).resize((int(avater_size*WR), int(avater_size*HR)))
        if avater_position == "l":
            base.paste(im=avatar, box=(int(avater_location[0]*WR), int(avater_location[1]*HR)), mask=get_round(avatar, int(avater_size*((WR+HR)/2)/5)))
        elif avater_position == "m":
            base.paste(im=avatar, box=(int(avater_location[0] - w/2) *WR, int(avater_location[1]*HR)), mask=get_round(avatar, int(avater_size*((WR+HR)/2)/5)))
        elif avater_position == "r":
            base.paste(im=avatar, box=(int((avater_location[0]-w)*WR), int(avater_location[1]*HR)), mask=get_round(avatar, int(avater_size*((WR+HR)/2)/5)))
    except:
        embed = disnake.Embed(
        title=f"오류 발생", description=f"유저의 아바타를 불러오는 과정에 오류가 발생하였습니다.\n문의해 주시기 바랍니다.\n오류 코드: 내정보10", color=0xFFB9B9)
        await inter.followup.send(embed=embed)
        return
        
    try:
        draw = ImageDraw.Draw(base)

        #name
        
        w = draw.textlength(text=inter.target.name+"#"+inter.target.discriminator, font=font_name)

        if name_position == "l":
            draw.text((name_location[0]*WR, name_location[1] *HR), inter.target.name+"#"+inter.target.discriminator, fill=hex_to_rgb(name_color), font=font_name)
        elif name_position == "m":
            draw.text(((name_location[0] - w/2) *WR, name_location[1] *HR), inter.target.name+"#"+inter.target.discriminator, fill=hex_to_rgb(name_color), font=font_name)
        elif name_position == "r":
            draw.text(((name_location[0] - w)*WR, name_location[1] *HR), inter.target.name+"#"+inter.target.discriminator, fill=hex_to_rgb(name_color), font=font_name)

        #money
        
        w = draw.textlength(text=str(money)+moneyName, font=font_money)

        if money_position == "l":
            draw.text((money_location[0]*WR, money_location[1] *HR), str(money)+moneyName, fill=hex_to_rgb(money_color), font=font_money)
        elif money_position == "m":
            draw.text(((money_location[0] - w/2)*WR, money_location[1] *HR), str(money)+moneyName, fill=hex_to_rgb(money_color), font=font_money)
        elif money_position == "r":
            draw.text(((money_location[0] - w)*WR, money_location[1] *HR), str(money)+moneyName, fill=hex_to_rgb(money_color), font=font_money)

        #chat
        
        w = draw.textlength(text=str(chat)+"회", font=font_info)

        if chat_position == "l":
            draw.text((chat_location[0]*WR, chat_location[1] *HR), str(chat)+"회", fill=hex_to_rgb(info_color), font=font_info)
        elif chat_position == "m":
            draw.text(((chat_location[0] - w/2)*WR, chat_location[1] *HR), str(chat)+"회", fill=hex_to_rgb(info_color), font=font_info)
        elif chat_position == "r":
            draw.text(((chat_location[0] - w)*WR, chat_location[1] *HR), str(chat)+"회", fill=hex_to_rgb(info_color), font=font_info)
        
        #voice
        
        w = draw.textlength(text=str(voice)+"분", font=font_info)

        if voice_position == "l":
            draw.text((voice_location[0]*WR, voice_location[1] *HR), str(voice)+"분", fill=hex_to_rgb(info_color), font=font_info)
        elif voice_position == "m":
            draw.text(((voice_location[0] - w/2)*WR, voice_location[1] *HR), str(voice)+"분", fill=hex_to_rgb(info_color), font=font_info)
        elif voice_position == "r":
            draw.text(((voice_location[0] - w)*WR, voice_location[1] *HR), str(voice)+"분", fill=hex_to_rgb(info_color), font=font_info)

        #attendance
        
        w = draw.textlength(text=str(attendance)+"회", font=font_info)

        if attendance_position == "l":
            draw.text((attendance_location[0]*WR, attendance_location[1] *HR), str(attendance)+"회", fill=hex_to_rgb(info_color), font=font_info)
        elif attendance_position == "m":
            draw.text(((attendance_location[0] - w/2)*WR, attendance_location[1] *HR), str(attendance)+"회", fill=hex_to_rgb(info_color), font=font_info)
        elif attendance_position == "r":
            draw.text(((attendance_location[0] - w)*WR, attendance_location[1] *HR), str(attendance)+"회", fill=hex_to_rgb(info_color), font=font_info)

        #activity
        
        w = draw.textlength(text=str(activity)+"시간", font=font_info)

        if activity_position == "l":
            draw.text((activity_location[0]*WR, activity_location[1] *HR), str(activity)+"시간", fill=hex_to_rgb(name_color), font=font_info)
        elif activity_position == "m":
            draw.text(((activity_location[0] - w/2)*WR, activity_location[1] *HR), str(activity)+"시간", fill=hex_to_rgb(name_color), font=font_info)
        elif activity_position == "r":
            draw.text(((activity_location[0] - w)*WR, activity_location[1] *HR), str(activity)+"시간", fill=hex_to_rgb(name_color), font=font_info)
    except:
        embed = disnake.Embed(
        title=f"오류 발생", description=f"이미지 생성중 오류가 발생하였습니다.\n문의해 주시기 바랍니다.\n오류 코드: 내정보11", color=0xFFB9B9)
        await inter.followup.send(embed=embed)
        return
    
    base.save("user.png")
    await inter.followup.send(file=disnake.File("user.png"))



@bot.slash_command(name="내")
async def money(inter):
    pass

@money.sub_command(name="정보", description="자신의 정보를 알려줍니다")
async def set(inter: disnake.ApplicationCommandInteraction):
    await inter.response.defer()
    try:
        with open(f'guild/{inter.guild.id}.json', encoding="utf-8") as f:
            json_object = json.load(f)
    except:
        embed = disnake.Embed(
            title=f"사용 불가", description=f"해당 서버는 이용 동의를 하지 않았습니다.\n동의를 완료한 서버에서 해당 메세지가 계속 나올 경우 문의를 해주시기 바랍니다.", color=0xFFB9B9)
        await inter.followup.send(embed=embed)
        return
    try:
        with open(f'guild/{inter.guild.id}.json', encoding="utf-8") as f:
            json_object = json.load(f)
            try:
                money = json_object['user'][str(inter.author.id)]["money"]
            except:
                money = 0
            try:
                chat = json_object['user'][str(inter.author.id)]["chat"]
            except:
                chat = 0
            try:
                voice = json_object['user'][str(inter.author.id)]["voice"]
            except:
                voice = 0
            try:
                attendance = json_object['user'][str(inter.author.id)]["attendance"]
            except:
                attendance = 0
            try:
                activity = json_object['user'][str(inter.author.id)]["activity"]
            except:
                activity = 0
            try:
                moneyName = json_object['setting']['moneyName']
            except:
                moneyName = "원"
            try:
                package = json_object['custom']['package']
                name_color = json_object["custom"]["color7"]
                money_color = json_object["custom"]["color8"]
                info_color = json_object["custom"]["color9"]
            except:
                embed = disnake.Embed(
                title=f"오류 발생", description=f"커스텀 데이터을 불러오는 과정에서 오류가 발생하였습니다.\n오류가 계속 될 경우 문의를 해주시기 바랍니다.\n오류 코드: 내정보1", color=0xFFB9B9)
                await inter.followup.send(embed=embed)
                return
    except:
        embed = disnake.Embed(
            title=f"오류 발생", description=f"데이터를 불러오는 과정에서 오류가 발생하였습니다.\n오류가 계속 될 경우 문의를 해주시기 바랍니다.\n오류 코드: 내정보2", color=0xFFB9B9)
        await inter.followup.send(embed=embed)
        return
    if moneyName == None:
        moneyName = "원"

    if package != "": #패키지
        try:
            with open(f'package/{package}.json', encoding="utf-8") as f:
                json_object = json.load(f)
                try:
                    avater_location = json_object["user_info"]["location1"]
                    avater_position = json_object["user_info"]["location1_position"]
                    avater_size = json_object["user_info"]["font_size1"]
                    name_location = json_object["user_info"]["location2"]
                    name_position = json_object["user_info"]["location2_position"]
                    money_location = json_object["user_info"]["location3"]
                    money_position = json_object["user_info"]["location3_position"]
                    chat_location = json_object["user_info"]["location4"]
                    chat_position = json_object["user_info"]["location4_position"]
                    voice_location = json_object["user_info"]["location5"]
                    voice_position = json_object["user_info"]["location5_position"]
                    attendance_location = json_object["user_info"]["location6"]
                    attendance_position = json_object["user_info"]["location6_position"]
                    activity_location = json_object["user_info"]["location7"]
                    activity_position = json_object["user_info"]["location7_position"]
                except:
                    embed = disnake.Embed(
                    title=f"오류 발생", description=f"글자의 위치를 불러오는데 오류가 발생하였습니다.\n문의해 주시기 바랍니다.\n오류 코드: 내정보3", color=0xFFB9B9)
                    await inter.followup.send(embed=embed)
                    return
                try:
                    name_font = json_object["user_info"]["font2"] #name
                    name_font_size = json_object["user_info"]["font_size2"]
                    name_color = json_object["user_info"]["color2"]
                    money_font = json_object["user_info"]["font3"] #money
                    money_font_size = json_object["user_info"]["font_size3"]
                    money_color = json_object["user_info"]["color3"]
                    info_font = json_object["user_info"]["font4"] #chat,voice,attendance,activity
                    info_font_size = json_object["user_info"]["font_size4"]
                    info_color = json_object["user_info"]["color4"]
                except:
                    embed = disnake.Embed(
                    title=f"오류 발생", description=f"글자의 폰트와 색상을 불러오는데 오류가 발생하였습니다.\n문의해 주시기 바랍니다.\n오류 코드: 내정보4", color=0xFFB9B9)
                    await inter.followup.send(embed=embed)
                    return
        except:
            embed = disnake.Embed(
            title=f"오류 발생", description=f"패키지 형식을 불러오는데 오류가 발생하였습니다.\n문의해 주시기 바랍니다.\n오류 코드: 내정보5", color=0xFFB9B9)
            await inter.followup.send(embed=embed)
            return

        try:
            img = Image.open(f"package/유저{package}.png")
            W, H = (img.width, img.height)
        except:
            embed = disnake.Embed(
                title=f"오류 발생", description=f"패키지의 이미지를 불러오지 못했습니다.\n오류가 계속 될 경우 문의해 주세요.\n오류 코드: 내정보6", color=0xFFB9B9)
            await inter.followup.send(embed=embed)
            return
    else: #기본&커스텀
        try:
            with open('package/nomal.json', encoding="utf-8") as f:
                json_object = json.load(f)
                try:
                    avater_location = json_object["user_info"]["location1"]
                    avater_position = json_object["user_info"]["location1_position"]
                    avater_size = json_object["user_info"]["font_size1"]
                    name_location = json_object["user_info"]["location2"]
                    name_position = json_object["user_info"]["location2_position"]
                    money_location = json_object["user_info"]["location3"]
                    money_position = json_object["user_info"]["location3_position"]
                    chat_location = json_object["user_info"]["location4"]
                    chat_position = json_object["user_info"]["location4_position"]
                    voice_location = json_object["user_info"]["location5"]
                    voice_position = json_object["user_info"]["location5_position"]
                    attendance_location = json_object["user_info"]["location6"]
                    attendance_position = json_object["user_info"]["location6_position"]
                    activity_location = json_object["user_info"]["location7"]
                    activity_position = json_object["user_info"]["location7_position"]
                except:
                    embed = disnake.Embed(
                    title=f"오류 발생", description=f"글자의 위치를 불러오는데 오류가 발생하였습니다.\n문의해 주시기 바랍니다.\n오류 코드: 내정보7", color=0xFFB9B9)
                    await inter.followup.send(embed=embed)
                    return
                try:
                    name_font = json_object["user_info"]["font2"] #name
                    name_font_size = json_object["user_info"]["font_size2"]
                    if name_color == "":
                        name_color = json_object["user_info"]["color2"]
                    money_font = json_object["user_info"]["font3"] #money
                    money_font_size = json_object["user_info"]["font_size3"]
                    if money_color == "":
                        money_color = json_object["user_info"]["color3"]
                    info_font = json_object["user_info"]["font4"] #chat,voice,attendance,activity
                    info_font_size = json_object["user_info"]["font_size4"]
                    if info_color == "":
                        info_color = json_object["user_info"]["color4"]
                except:
                    embed = disnake.Embed(
                    title=f"오류 발생", description=f"글자의 폰트와 색상을 불러오는데 오류가 발생하였습니다.\n문의해 주시기 바랍니다.\n오류 코드: 내정보8", color=0xFFB9B9)
                    await inter.followup.send(embed=embed)
                    return

        except:
            embed = disnake.Embed(
                title=f"오류 발생", description=f"기본 형식을 불러오는데 오류가 발생하였습니다.\n문의해 주시기 바랍니다.\n오류 코드: 내정보9", color=0xFFB9B9)
            await inter.followup.send(embed=embed)
            return

        try:
            img = Image.open(f"custom/유저{inter.guild.id}.png")
        except:
            img = Image.open("DISTORE_user.png")

        W, H = (img.width, img.height)

        if package == "":
            WR = W/3200
            HR = H/1800
            print("유저배율:" + str(WR) + "," + str(HR))
            name_len = len(inter.author.name+"#"+inter.author.discriminator) 
            font_name = ImageFont.truetype(name_font, int(name_font_size*WR+15-name_len*1.7))
            font_money = ImageFont.truetype(money_font, int(money_font_size*WR))
            font_info = ImageFont.truetype(info_font, int(info_font_size*WR))
        else:
            WR = 1

    #avater
    base = Image.new('RGBA',size=(W,H))

    base.paste(img, (0,0))

    w = avater_size*WR

    try:
        try:
            avatar = Image.open(io.BytesIO(requests.get(inter.author.avatar).content)).resize((int(avater_size*WR), int(avater_size*HR)))
        except:
            avatar = Image.open(io.BytesIO(requests.get(inter.author.default_avatar).content)).resize((int(avater_size*WR), int(avater_size*HR)))
        if avater_position == "l":
            base.paste(im=avatar, box=(int(avater_location[0]*WR), int(avater_location[1]*HR)), mask=get_round(avatar, int(avater_size*((WR+HR)/2)/5)))
        elif avater_position == "m":
            base.paste(im=avatar, box=(int(avater_location[0] - w/2) *WR, int(avater_location[1]*HR)), mask=get_round(avatar, int(avater_size*((WR+HR)/2)/5)))
        elif avater_position == "r":
            base.paste(im=avatar, box=(int((avater_location[0]-w)*WR), int(avater_location[1]*HR)), mask=get_round(avatar, int(avater_size*((WR+HR)/2)/5)))
    except:
        embed = disnake.Embed(
        title=f"오류 발생", description=f"유저의 아바타를 불러오는 과정에 오류가 발생하였습니다.\n문의해 주시기 바랍니다.\n오류 코드: 내정보10", color=0xFFB9B9)
        await inter.followup.send(embed=embed)
        return
        
    try:
        draw = ImageDraw.Draw(base)

        #name
        
        w = draw.textlength(text=inter.author.name+"#"+inter.author.discriminator, font=font_name)

        if name_position == "l":
            draw.text((name_location[0]*WR, name_location[1] *HR), inter.author.name+"#"+inter.author.discriminator, fill=hex_to_rgb(name_color), font=font_name)
        elif name_position == "m":
            draw.text(((name_location[0] - w/2) *WR, name_location[1] *HR), inter.author.name+"#"+inter.author.discriminator, fill=hex_to_rgb(name_color), font=font_name)
        elif name_position == "r":
            draw.text(((name_location[0] - w)*WR, name_location[1] *HR), inter.author.name+"#"+inter.author.discriminator, fill=hex_to_rgb(name_color), font=font_name)

        #money
        
        w = draw.textlength(text=str(money)+moneyName, font=font_money)

        if money_position == "l":
            draw.text((money_location[0]*WR, money_location[1] *HR), str(money)+moneyName, fill=hex_to_rgb(money_color), font=font_money)
        elif money_position == "m":
            draw.text(((money_location[0] - w/2)*WR, money_location[1] *HR), str(money)+moneyName, fill=hex_to_rgb(money_color), font=font_money)
        elif money_position == "r":
            draw.text(((money_location[0] - w)*WR, money_location[1] *HR), str(money)+moneyName, fill=hex_to_rgb(money_color), font=font_money)

        #chat
        
        w = draw.textlength(text=str(chat)+"회", font=font_info)

        if chat_position == "l":
            draw.text((chat_location[0]*WR, chat_location[1] *HR), str(chat)+"회", fill=hex_to_rgb(info_color), font=font_info)
        elif chat_position == "m":
            draw.text(((chat_location[0] - w/2)*WR, chat_location[1] *HR), str(chat)+"회", fill=hex_to_rgb(info_color), font=font_info)
        elif chat_position == "r":
            draw.text(((chat_location[0] - w)*WR, chat_location[1] *HR), str(chat)+"회", fill=hex_to_rgb(info_color), font=font_info)
        
        #voice
        
        w = draw.textlength(text=str(voice)+"분", font=font_info)

        if voice_position == "l":
            draw.text((voice_location[0]*WR, voice_location[1] *HR), str(voice)+"분", fill=hex_to_rgb(info_color), font=font_info)
        elif voice_position == "m":
            draw.text(((voice_location[0] - w/2)*WR, voice_location[1] *HR), str(voice)+"분", fill=hex_to_rgb(info_color), font=font_info)
        elif voice_position == "r":
            draw.text(((voice_location[0] - w)*WR, voice_location[1] *HR), str(voice)+"분", fill=hex_to_rgb(info_color), font=font_info)

        #attendance
        
        w = draw.textlength(text=str(attendance)+"회", font=font_info)

        if attendance_position == "l":
            draw.text((attendance_location[0]*WR, attendance_location[1] *HR), str(attendance)+"회", fill=hex_to_rgb(info_color), font=font_info)
        elif attendance_position == "m":
            draw.text(((attendance_location[0] - w/2)*WR, attendance_location[1] *HR), str(attendance)+"회", fill=hex_to_rgb(info_color), font=font_info)
        elif attendance_position == "r":
            draw.text(((attendance_location[0] - w)*WR, attendance_location[1] *HR), str(attendance)+"회", fill=hex_to_rgb(info_color), font=font_info)

        #activity
        
        w = draw.textlength(text=str(activity)+"시간", font=font_info)

        if activity_position == "l":
            draw.text((activity_location[0]*WR, activity_location[1] *HR), str(activity)+"시간", fill=hex_to_rgb(name_color), font=font_info)
        elif activity_position == "m":
            draw.text(((activity_location[0] - w/2)*WR, activity_location[1] *HR), str(activity)+"시간", fill=hex_to_rgb(name_color), font=font_info)
        elif activity_position == "r":
            draw.text(((activity_location[0] - w)*WR, activity_location[1] *HR), str(activity)+"시간", fill=hex_to_rgb(name_color), font=font_info)
    except:
        embed = disnake.Embed(
        title=f"오류 발생", description=f"이미지 생성중 오류가 발생하였습니다.\n문의해 주시기 바랍니다.\n오류 코드: 내정보11", color=0xFFB9B9)
        await inter.followup.send(embed=embed)
        return
    
    base.save("user.png")
    await inter.followup.send(file=disnake.File("user.png"))

@bot.slash_command(name="초기화", description="서버의 모든 데이터를 초기화합니다.")
@commands.default_member_permissions(administrator=True)
async def list(inter: disnake.ApplicationCommandInteraction):
    await inter.response.defer(ephemeral=True)
    os.remove(f"guild/{inter.guild.id}.json")
    await inter.followup.send("파일은 삭제하였지만 아직 미완성인 명령어입니다")

@bot.slash_command(name="돈관리")
@commands.default_member_permissions(administrator=True)
async def moneyad(inter):
    pass

@moneyad.sub_command(name="지급", description="유저에게 돈을 지급합니다.")
async def set(inter: disnake.ApplicationCommandInteraction, 유저: disnake.User, 금액: commands.Range[-10000000, 10000000]):
    """
    유저에게 돈을 지급합니다.

    Parameters
    ----------
    유저: 돈을 지급할 유저
    금액: 지급할 금액
    """
    await inter.response.defer(ephemeral=True)
    if 유저.bot:
        embed = disnake.Embed(
            title=f"봇에게는 지급이 불가합니다.", description=f"", color=0xFFB9B9)
        await inter.followup.send.send(embed=embed)
        return
    try:
        with open(f'guild/{inter.guild.id}.json', encoding="utf-8") as f:
            json_object = json.load(f)
    except:
        embed = disnake.Embed(
        title=f"사용 불가", description=f"해당 서버는 이용 동의를 하지 않았습니다.\n동의를 완료한 서버에서 해당 메세지가 계속 나올 경우 문의를 해주시기 바랍니다.", color=0xFFB9B9)
        await inter.followup.send(embed=embed)
        return
    try:
        with open(f'guild/{inter.guild.id}.json', encoding="utf-8") as f:
            json_object = json.load(f)
            logchannel = json_object['setting']["logChannel"]
            json_object['user'][str(유저.id)]["money"] += 금액
            if json_object['user'][str(유저.id)]["money"] < 0:
                json_object['user'][str(유저.id)]["money"] = 0
            money = json_object['user'][str(유저.id)]["money"]
            moneyName = json_object['setting']['moneyName']
    except:
        embed = disnake.Embed(
        title=f"오류 발생", description=f"데이터를 불러오는 과정에서 오류가 발생하였습니다.\n오류가 계속 될 경우 문의를 해주시기 바랍니다.", color=0xFFB9B9)
        await inter.followup.send(embed=embed)
        return
    try:
        with open(f'guild/{inter.guild.id}.json', 'w', encoding="utf-8") as f:
            json.dump(json_object, f, indent=2, ensure_ascii=False)
    except:
        embed = disnake.Embed(
        title=f"오류 발생", description=f"데이터를 저장하는 과정에서 오류가 발생하였습니다.\n오류가 계속 될 경우 문의를 해주시기 바랍니다.", color=0xFFB9B9)
        await inter.followup.send(embed=embed)
        return
    embed = disnake.Embed(
        title=f"{유저}님에게 지급완료", description=f"지급된 금액 : `{금액}`{moneyName}\n현재 보유금액 : `{money}`{moneyName}", color=0xFFB9B9)
    await inter.followup.send(embed=embed)
    if logchannel != 0 and type(logchannel) == int:
        embed = disnake.Embed(
            title=f"{유저}님에게 지급완료", description=f"지급된 금액 : `{금액}`{moneyName}\n현재 보유금액 : `{money}`{moneyName}\n명령어 사용자: {inter.author.mention}", color=0xFFB9B9)
        await bot.get_channel(logchannel).send(embed=embed)
    





@bot.slash_command(name="상품관리")
@commands.default_member_permissions(administrator=True)
async def goods_ad(inter):
    pass


@goods_ad.sub_command(name="추가")
async def goods_add(inter: disnake.ApplicationCommandInteraction, 상품: commands.String[1, 16], 값: commands.Range[1, 10000000000], 재고 : commands.Range[1, 100000]=None, 설명 : commands.String[1, 30]=None, 역할 : disnake.Role=None, 텍스트 : commands.String[1, 50]=None):
    """
    상품을 추가하거나 수정합니다.

    Parameters
    ----------
    상품: 상품의 이름
    값: 판매하려는 가격
    재고: 판매하려는 개수
    설명: 상품의 설명
    역할: 상품을 구매시 지급 될 역할
    텍스트: 상품을 구매해야만 알 수 있는 내용입니다
    """
    await inter.response.defer(ephemeral=True)
    try:
        with open(f'guild/{inter.guild.id}.json', encoding="utf-8") as f:
            json_object = json.load(f)
    except:
        embed = disnake.Embed(
        title=f"사용 불가", description=f"해당 서버는 이용 동의를 하지 않았습니다.\n동의를 완료한 서버에서 해당 메세지가 계속 나올 경우 문의를 해주시기 바랍니다.", color=0xFFB9B9)
        await inter.followup.send(embed=embed)
        return
    good_name = 상품

    if 재고 == None:
        재고 = "무한"
    if 설명 == None:
        설명 = "없음"
    if 역할 == None:
        역할 = "`없음`"
    else:
        역할 = 역할.id
    if 텍스트 == None:
        텍스트 = "없음"

    try:
        with open(f'guild/{inter.guild.id}.json', encoding="utf-8") as f:
            json_object = json.load(f)
            premium = json_object["premium"]["expiration_date"]
    except:
        embed = disnake.Embed(
        title=f"오류 발생", description=f"데이터를 불러오는 과정에서 오류가 발생하였습니다\n오류가 계속 될 경우 문의를 해주시기 바랍니다.", color=0xFFB9B9)
        await inter.followup.send(embed=embed)
        return
    if good_name == "테스트" or korcen.check(good_name):
        embed = disnake.Embed(
            title=f"추가 할 수 없는 상품입니다", description=f"이름이 `테스트`이거나 비속어가 들어가 있다면 상풍을 추가 할 수 없습니다.", color=0xFFB9B9)
        await inter.followup.send(embed=embed)
        return
    try:
        with open(f'guild/{inter.guild.id}.json', encoding="utf-8") as f:
            json_object = json.load(f)
            moneyName = json_object["setting"]["moneyName"]
    except:
        embed = disnake.Embed(
            title=f"오류 발생", description=f"데이터를 불러오는 과정에서 오류가 발생하였습니다\n오류가 계속 될 경우 문의를 해주시기 바랍니다.", color=0xFFB9B9)
        await inter.followup.send(embed=embed)
        return
    try:
        with open(f'guild/{inter.guild.id}.json', encoding="utf-8") as f:
            json_object = json.load(f)
            description = json_object["goods"][str(good_name)]["description"]
            roleId = json_object["goods"][str(good_name)]["roleId"]
            text = json_object["goods"][str(good_name)]["text"]
            remain = json_object["goods"][str(good_name)]["remain"]
            good_price = json_object["goods"][str(good_name)]["good_price"]
            json_object["goods"][str(good_name)]["description"] = 설명
            json_object["goods"][str(good_name)]["roleId"] = 역할
            json_object["goods"][str(good_name)]["text"] = 텍스트
            json_object["goods"][str(good_name)]["remain"] = 재고
            json_object["goods"][str(good_name)]["good_price"] = 값
        good = 1
    except:
        good = 0
    if good == 1:
        try:
            with open(f'guild/{inter.guild.id}.json', 'w', encoding="utf-8") as f:
                json.dump(json_object, f, indent=2, ensure_ascii=False)
        except:
            embed = disnake.Embed(
            title=f"오류 발생", description=f"데이터를 저장하는 과정에서 오류가 발생하였습니다.\n오류가 계속 될 경우 문의를 해주시기 바랍니다.", color=0xFFB9B9)
            await inter.followup.send(embed=embed)
            return
        if type(roleId) == int:
            try:
                role = disnake.utils.get(inter.guild.roles, id=roleId).mention
            except:
                role = "오류"
        else:
            role = "없음"
        if type(역할) == int:
            try:
                역할 = disnake.utils.get(inter.guild.roles, id=roleId).mention
            except:
                역할 = "오류"
        embed = disnake.Embed(
            title=f"상품 수정", description=f"기존에 있던 품목을 수정하였습니다\n이름 : `{good_name}`\n가격 : `{good_price}`{moneyName} > `{값}`{moneyName}\n설명 : `{description}` > `{설명}`", color=0xFFB9B9)
        embed.add_field(
            name=f"재고", value=f"`{remain}`개 > `{재고}`개", inline=False)
        embed.add_field(
            name=f"지급 역할", value=f"{role} > {역할}", inline=False)
        embed.add_field(
            name=f"지급 텍스트", value=f"`{text}` > `{텍스트}`", inline=False)

        
        await inter.followup.send(embed=embed)
    else:
        try:
            with open(f'guild/{inter.guild.id}.json', encoding="utf-8") as f:
                json_object = json.load(f)
                goods = json_object["goods"]

        except:
            embed = disnake.Embed(
            title=f"오류 발생", description=f"데이터를 불러오는 과정에서 오류가 발생하였습니다.\n오류가 계속 될 경우 문의를 해주시기 바랍니다.", color=0xFFB9B9)
            await inter.followup.send(embed=embed)
            return
        if len(goods) >= 20:
            embed = disnake.Embed(
                title=f"추가 불가", description=f"추가 가능한 상품 개수를 초과하였습니다.\n다른 상품을 삭제하시거나 프리미엄을 이용하세요.", color=0xFFB9B9)
            await inter.followup.send(embed=embed)
            return
        else:
            with open(f'guild/{inter.guild.id}.json', encoding="utf-8") as f:
                json_object = json.load(f)
                json_object["goods"][str(good_name)] = {}
                json_object["goods"][str(good_name)]["description"] = 설명
                json_object["goods"][str(good_name)]["roleId"] = 역할
                json_object["goods"][str(good_name)]["text"] = 텍스트
                json_object["goods"][str(good_name)]["remain"] = 재고
                json_object["goods"][str(good_name)]["good_price"] = 값
                json_object["goods"][str(good_name)]["time"] = str(time.localtime(time.time()).tm_year)+"년 "+str(time.localtime(time.time()).tm_mon)+"월 "+str(time.localtime(time.time()).tm_mday)+"일 "+str(time.localtime(time.time()).tm_hour)+"시 "+str(time.localtime(time.time()).tm_min)+"분"
                json_object["goods"][str(good_name)]["goodcount"] = 0

            try:
                with open(f'guild/{inter.guild.id}.json', 'w', encoding="utf-8") as f:
                    json.dump(json_object, f, indent=2, ensure_ascii=False)
            except:
                embed = disnake.Embed(
                title=f"오류 발생", description=f"데이터를 저장하는 과정에서 오류가 발생하였습니다.\n오류가 계속 될 경우 문의를 해주시기 바랍니다.", color=0xFFB9B9)
                await inter.followup.send(embed=embed)
                return

            if type(역할) == int:
                try:
                    역할 = disnake.utils.get(inter.guild.roles, id=roleId).mention
                except:
                    역할 = "오류"

            embed = disnake.Embed(
                title=f"새로운 상품 추가!", description=f"이름 : {good_name}\n가격 : `{값}`{moneyName}", color=0xFFB9B9)
            embed.add_field(
                    name=f"설명", value=f"`{설명}`", inline=False)
            embed.add_field(
                    name=f"재고", value=f"`{재고}`개", inline=False)
            embed.add_field(
                    name=f"지급 역할", value=f"{역할}", inline=False)
            embed.add_field(
                        name=f"지급 텍스트", value=f"{텍스트}", inline=False)
            await inter.followup.send(embed=embed)


async def autocomp_goods(inter: disnake.ApplicationCommandInteraction, user_input: str):
    try:
        with open(f'guild/{inter.guild.id}.json', encoding="utf-8") as f:
            json_object = json.load(f)
            goods = json_object["goods"]
    except:
        goods = []
    return [good for good in goods if user_input in good]

@goods_ad.sub_command(name="삭제", description="상품을 삭제합니다.")
async def goods_del(inter: disnake.ApplicationCommandInteraction, 상품: str = commands.Param(autocomplete=autocomp_goods)):
    """
    상품을 삭제합니다.

    Parameters
    ----------
    상품: 삭제하려는 상품
    """
    await inter.response.defer(ephemeral=True)
    try:
        with open(f'guild/{inter.guild.id}.json', encoding="utf-8") as f:
            json_object = json.load(f)
    except:
        embed = disnake.Embed(
        title=f"사용 불가", description=f"해당 서버는 이용 동의를 하지 않았습니다.\n동의를 완료한 서버에서 해당 메세지가 계속 나올 경우 문의를 해주시기 바랍니다.", color=0xFFB9B9)
        await inter.followup.send(embed=embed)
        return
    good_name = 상품
    try:
        with open(f'guild/{inter.guild.id}.json', encoding="utf-8") as f:
            json_object = json.load(f)
            good_price = json_object["goods"][str(good_name)]["good_price"]
    except:
        good_price = None

        
    if good_price != None:
        with open(f'guild/{inter.guild.id}.json', encoding="utf-8") as f:
            json_object = json.load(f)
            good_price = json_object["goods"].pop(str(good_name))
        try:
            with open(f'guild/{inter.guild.id}.json', 'w', encoding="utf-8") as f:
                json.dump(json_object, f, indent=2, ensure_ascii=False)
        except:
            embed = disnake.Embed(
            title=f"오류 발생", description=f"데이터를 저장하는 과정에서 오류가 발생하였습니다.\n오류가 계속 될 경우 문의를 해주시기 바랍니다.", color=0xFFB9B9)
            await inter.followup.send(embed=embed)
            return
        embed = disnake.Embed(
            title=f"상품을 삭제했습니다", description=f"{good_name} 품목을 삭제했습니다", color=0xFFB9B9)
        await inter.followup.send(embed=embed)
    else:
        embed = disnake.Embed(
            title=f"오류 발생", description=f"존재하지 않는 상품입니다.\n오류가 계속 될 경우 문의를 해주시기 바랍니다.", color=0xFFB9B9)
        await inter.followup.send(embed=embed)


@bot.slash_command(name="상품")
async def goods(inter):
    pass

async def autocomp_goods(inter: disnake.ApplicationCommandInteraction, user_input: str):
    try:
        with open(f'guild/{inter.guild.id}.json', encoding="utf-8") as f:
            json_object = json.load(f)
            goods = json_object["goods"]
    except:
        goods = []
    return [good for good in goods if user_input in good]


@goods.sub_command(name="구매", description="상품을 구매합니다.")
async def buy(inter: disnake.ApplicationCommandInteraction, 상품: str = commands.Param(autocomplete=autocomp_goods)):
    """
    상품을 구매합니다.

    Parameters
    ----------
    상품: 구매하려는 상품
    """
    await inter.response.defer()
    try:
        with open(f'guild/{inter.guild.id}.json', encoding="utf-8") as f:
            json_object = json.load(f)
    except:
        embed = disnake.Embed(
        title=f"사용 불가", description=f"해당 서버는 이용 동의를 하지 않았습니다.\n동의를 완료한 서버에서 해당 메세지가 계속 나올 경우 문의를 해주시기 바랍니다.", color=0xFFB9B9)
        await inter.followup.send(embed=embed)
        return
    good_name = 상품
    try:
        with open(f'guild/{inter.guild.id}.json', encoding="utf-8") as f:
            json_object = json.load(f)
            try:
                goods = json_object["goods"][good_name]
            except:
                embed = disnake.Embed(
                    title=f"오류 발생", description=f"존재하지 않는 상품입니다.\n`/상품 목록`으로 상품을 확인해 보세요\n\n오류가 계속 될 경우 문의를 해주시기 바랍니다.\n오류 코드: 구매1", color=0xFFB9B9)
                await inter.followup.send(embed=embed)
                return
            try:
                good_price = json_object["goods"][good_name]["good_price"]
                remain = json_object["goods"][good_name]["remain"]
                if remain == "무한":
                    remain = 10001
                else:
                    remain = remain
                text = json_object["goods"][good_name]["text"]
                goodcount = json_object["goods"][good_name]["goodcount"]
                roleId = json_object["goods"][good_name]["roleId"]
            except:
                embed = disnake.Embed(
                    title=f"오류 발생", description=f"상품의 정보를 불러오는데 오류가 발생하였습니다.\n문의해 주시기 바랍니다.\n오류 코드: 구매2", color=0xFFB9B9)
                await inter.followup.send(embed=embed)
                return
        try:
            money = json_object["user"][str(inter.author.id)]["money"]
        except:
            embed = disnake.Embed(
                title=f"오류 발생", description=f"유저의 정보를 불러오는데 오류가 발생하였습니다.\n오류가 계속 될 경우 문의를 해주시기 바랍니다.\n오류 코드: 구매3", color=0xFFB9B9)
            await inter.followup.send(embed=embed)
            return
        try:
            package = json_object['custom']['package']
            user_color = json_object["custom"]["color10"]
            text1_color = json_object["custom"]["color11"] #goods name
            text2_color = json_object["custom"]["color12"] #text
            text3_color = json_object["custom"]["color13"] #price
            text4_color = json_object["custom"]["color14"] #role
            moneyName = json_object["setting"]["moneyName"]
            logchannel = json_object["setting"]["logChannel"]
        except:
            embed = disnake.Embed(
                title=f"오류 발생", description=f"설정 정보를 불러오는데 오류가 발생하였습니다.\n오류가 계속 될 경우 문의를 해주시기 바랍니다.\n오류 코드: 구매3", color=0xFFB9B9)
            await inter.followup.send(embed=embed)
            return

    except:
        embed = disnake.Embed(
                title=f"오류 발생", description=f"데이터를 불러오는 과정에서 오류가 발생하였습니다.\n오류가 계속 될 경우 문의를 해주시기 바랍니다.\n오류 코드: 구매4", color=0xFFB9B9)
        await inter.followup.send(embed=embed)

    if remain <= 0: #재고 확인
        embed = disnake.Embed(
            title=f"재고 없음", description=f"`{good_name}` 품목은 남은 재고가 없습니다", color=0xFFB9B9)
        await inter.followup.send(embed=embed)
        return

    elif money < good_price: #돈 확인
        embed = disnake.Embed(
            title=f"돈이 부족합니다.", description=f"보유금 : `{money}`{moneyName}\n상품금액 : `{good_price}`{moneyName}", color=0xFFB9B9)
        await inter.followup.send(embed=embed)
    else:
        json_object["user"][str(inter.author.id)]["money"] -= good_price
        if roleId != "`없음`" and type(roleId) == int:
            role = disnake.utils.get(inter.guild.roles, id=roleId)
        else:
            role = None
        if goodcount == None:
            goodcount = 0
        if remain < 10001:
            try:
                if 0 < remain < 10001:
                    json_object["goods"][good_name]["remain"] -= 1
                json_object["goods"][good_name]["goodcount"] += 1
                with open(f'guild/{inter.guild.id}.json', 'w', encoding="utf-8") as f:
                    json.dump(json_object, f, indent=2, ensure_ascii=False)
            except:
                embed = disnake.Embed(
                title=f"오류 발생", description=f"데이터를 저장하는 과정에서 오류가 발생하였습니다.\n오류가 계속 될 경우 문의를 해주시기 바랍니다.오류 코드: 구매5", color=0xFFB9B9)
                await inter.followup.send(embed=embed)
                return
            embed = disnake.Embed(
                title=f"상품 구매 성공!", description=f"{good_name} 품목을 `{good_price}`{moneyName}에 구입하였습니다.\n남은 재고 : `{remain-1}`개\n현재 보유금 : `{money-good_price}`{moneyName}", color=0xFFB9B9)
        else:
            try:
                if 0 < remain < 10001:
                    json_object["goods"][good_name]["remain"] -= 1
                json_object["goods"][good_name]["goodcount"] += 1
                with open(f'guild/{inter.guild.id}.json', 'w', encoding="utf-8") as f:
                    json.dump(json_object, f, indent=2, ensure_ascii=False)
            except:
                embed = disnake.Embed(
                title=f"오류 발생", description=f"데이터를 저장하는 과정에서 오류가 발생하였습니다.\n오류가 계속 될 경우 문의를 해주시기 바랍니다.\n오류 코드: 구매6", color=0xFFB9B9)
                await inter.followup.send(embed=embed)
                return
            embed = disnake.Embed(
                title=f"상품 구매 성공!", description=f"{good_name} 품목을 `{good_price}`{moneyName}에 구입하였습니다.\n현재 보유금 : `{money-good_price}`{moneyName}", color=0xFFB9B9)
        try:
            if role != None:
                await inter.author.add_roles(role)
        except:
            await inter.followup.send("역할 지급이 실패하였습니다.\n권한 문제이거나 오류일 수 있습니다.\n서버에 문의하세요\n오류 코드: 구매7")
        embed.set_footer(text="구매 확인서는 DM으로 전송됩니다.")
        await inter.followup.send(embed=embed)
        try:
            embed = disnake.Embed(
                title=f"구매 확인서", description=f"구매 품목 : {good_name}\n가격 : {good_price}\n구매 번호 : {goodcount+1}{inter.author.id}{int(time.time())}", color=0xFFB9B9)
            if text != "없음":
                en = ["q","w","e","r","t","y","u","i","o","p","l","k","j","h","g","f","d","s","a","z","x","c","v","b","n","m"]
                text = re.sub("(시간)", f"{int(time.time())}", text)
                text = re.sub("(랜덤 숫자)", f"{random.randint(0,9)}", text)
                text = re.sub("(랜덤 영어)", f"{random.choice(en)}", text)

            if package != "": #패키지
                try:
                    with open(f'package/{package}.json', encoding="utf-8") as f:
                        json_object = json.load(f)
                        user_location = json_object["buy_check"]["location1"]
                        user_position = json_object["buy_check"]["location1_position"]
                        goods_name_location = json_object["buy_check"]["location2"]
                        goods_name_position = json_object["buy_check"]["location2_position"]
                        goods_price_location = json_object["buy_check"]["location3"]
                        goods_price_position = json_object["buy_check"]["location3_position"]
                        role_location = json_object["buy_check"]["location4"]
                        role_position = json_object["buy_check"]["location4_position"]
                        goods_text_location = json_object["buy_check"]["location5"]
                        goods_text_position = json_object["buy_check"]["location5_position"]
                        user_font = json_object["buy_check"]["font1"] #user
                        user_font_size = json_object["buy_check"]["font_size1"]
                        user_color = json_object["buy_check"]["color1"]
                        text1_font = json_object["buy_check"]["font2"] #goods name
                        text1_font_size = json_object["buy_check"]["font_size2"]
                        text1_color = json_object["buy_check"]["color2"]
                        text2_font = json_object["buy_check"]["font3"] #price
                        text2_font_size = json_object["buy_check"]["font_size3"]
                        text2_color = json_object["buy_check"]["color3"]
                        text3_font = json_object["buy_check"]["font4"] #role
                        text3_font_size = json_object["buy_check"]["font_size4"]
                        text3_color = json_object["buy_check"]["color4"]
                        text4_font = json_object["buy_check"]["font5"] #text
                        text4_font_size = json_object["buy_check"]["font_size5"]
                        text4_color = json_object["buy_check"]["color5"]


                except:
                    embed = disnake.Embed(
                    title=f"오류 발생", description=f"패키지 형식을 불러오는데 오류가 발생하였습니다.\n문의해 주시기 바랍니다.\n오류 코드: 목록2", color=0xFFB9B9)
                    await inter.followup.send(embed=embed)
                    return

                try:
                    img = Image.open(f"package/목록{package}.png")
                    W, H = (img.width, img.height)
                except:
                    embed = disnake.Embed(
                        title=f"오류 발생", description=f"패키지의 이미지를 불러오지 못했습니다.\n오류가 계속 될 경우 문의해 주세요.\n오류 코드: 목록3", color=0xFFB9B9)
                    await inter.followup.send(embed=embed)
                    return
            else: #기본&커스텀
                try:
                    with open('package/nomal.json', encoding="utf-8") as f:
                        json_object = json.load(f)
                        user_location = json_object["buy_check"]["location1"]
                        user_position = json_object["buy_check"]["location1_position"]
                        goods_name_location = json_object["buy_check"]["location2"]
                        goods_name_position = json_object["buy_check"]["location2_position"]
                        goods_price_location = json_object["buy_check"]["location3"]
                        goods_price_position = json_object["buy_check"]["location3_position"]
                        role_location = json_object["buy_check"]["location4"]
                        role_position = json_object["buy_check"]["location4_position"]
                        goods_text_location = json_object["buy_check"]["location5"]
                        goods_text_position = json_object["buy_check"]["location5_position"]
                        user_font = json_object["buy_check"]["font1"] #user
                        user_font_size = json_object["buy_check"]["font_size1"]
                        if user_color == "":
                            user_color = json_object["buy_check"]["color1"]
                        text1_font = json_object["buy_check"]["font2"] #goods name
                        text1_font_size = json_object["buy_check"]["font_size2"]
                        if text1_color == "":
                            text1_color = json_object["buy_check"]["color2"]
                        text2_font = json_object["buy_check"]["font3"] #price
                        text2_font_size = json_object["buy_check"]["font_size3"]
                        if text2_color == "":
                            text2_color = json_object["buy_check"]["color3"]
                        text3_font = json_object["buy_check"]["font4"] #role
                        text3_font_size = json_object["buy_check"]["font_size4"]
                        if text3_color == "":
                            text3_color = json_object["buy_check"]["color4"]
                        text4_font = json_object["buy_check"]["font5"] #text
                        text4_font_size = json_object["buy_check"]["font_size5"]
                        if text4_color == "":
                            text4_color = json_object["buy_check"]["color5"]

                except:
                    embed = disnake.Embed(
                        title=f"오류 발생", description=f"기본 형식을 불러오는데 오류가 발생하였습니다.\n문의해 주시기 바랍니다.\n오류 코드: 목록4", color=0xFFB9B9)
                    await inter.followup.send(embed=embed)
                    return

                try:
                    img = Image.open(f"custom/구매{inter.guild.id}.png")
                except:
                    img = Image.open("DISTORE_buy.png")

                W, H = (img.width, img.height)

                if package == "":
                    WR = W/3200
                    HR = H/1800
                    print("구매확인서배율:" + str(WR) + "," + str(HR))
                    user_len = len(inter.author.name+"#"+inter.author.discriminator)
                    text_len = len(text)
                    good_len = len(good_name)
                    if user_len >= 18:
                        font_user = ImageFont.truetype(user_font, int(user_font_size-45*WR))
                    else:
                        font_user = ImageFont.truetype(user_font, int(user_font_size*WR+15*WR-user_len*3*WR))
                    font_1 = ImageFont.truetype(text1_font, int(text1_font_size*WR+15*WR-good_len*3*WR))
                    font_2 = ImageFont.truetype(text2_font, int(text2_font_size*WR))
                    font_3 = ImageFont.truetype(text3_font, int(text3_font_size*WR))
                    if text_len>=25 :
                        font_4 = ImageFont.truetype(text4_font, int(text4_font_size*WR+15*WR-100))
                    else:
                        font_4 = ImageFont.truetype(text4_font, int(text4_font_size*WR+15*WR-text_len*3))
                else:
                    WR = 1
                    HR = 1

            draw = ImageDraw.Draw(img)

            #user
            if user_len <= 18:
                w = draw.textlength(text=inter.author.name+"#"+inter.author.discriminator, font=font_user) 

                if user_position == "l":
                    draw.text((user_location[0]*WR, user_location[1] *HR), inter.author.name+"#"+inter.author.discriminator, fill=hex_to_rgb(user_color), font=font_user)
                elif user_position == "m":
                    draw.text(((user_location[0]*WR - w/2), user_location[1] *HR), inter.author.name+"#"+inter.author.discriminator, fill=hex_to_rgb(user_color), font=font_user)
                elif user_position == "r":
                    draw.text(((user_location[0]*WR - w), user_location[1] *HR), inter.author.name+"#"+inter.author.discriminator, fill=hex_to_rgb(user_color), font=font_user)
            else:
                name = inter.author.name+"#"+inter.author.discriminator
                cut = int(user_len/2)
                w = draw.textlength(text=name[0:cut], font=font_user) 
                name = name[0:cut] + "\n" + name[cut:]

                if user_position == "l":
                    draw.multiline_text((user_location[0]*WR, user_location[1] *HR), name, fill=hex_to_rgb(user_color), font=font_user)
                elif user_position == "m":
                    draw.multiline_text(((user_location[0]*WR - w/2), user_location[1] *HR), name, fill=hex_to_rgb(user_color), font=font_user, align='center')
                elif user_position == "r":
                    draw.multiline_text(((user_location[0]*WR - w), user_location[1] *HR), name, fill=hex_to_rgb(user_color), font=font_user, align='right')

            #goods name
            w = draw.textlength(text=good_name, font=font_1) 
            
            if goods_name_position == "l":
                draw.text((goods_name_location[0]*WR, goods_name_location[1] *HR), good_name, fill=hex_to_rgb(text1_color), font=font_1)
            elif goods_name_position == "m":
                draw.text(((goods_name_location[0]*WR - w/2), goods_name_location[1] *HR), good_name, fill=hex_to_rgb(text1_color), font=font_1)
            elif goods_name_position == "r":
                draw.text(((goods_name_location[0]*WR - w), goods_name_location[1] *HR), good_name, fill=hex_to_rgb(text1_color), font=font_1)

            #price
            w = draw.textlength(text=str(good_price)+moneyName, font=font_2) 
            
            if goods_price_position == "l":
                draw.text((goods_price_location[0]*WR, goods_price_location[1] *HR), str(good_price)+moneyName, fill=hex_to_rgb(text2_color), font=font_2)
            elif goods_price_position == "m":
                draw.text(((goods_price_location[0]*WR - w/2), goods_price_location[1] *HR), str(good_price)+moneyName, fill=hex_to_rgb(text2_color), font=font_2)
            elif goods_price_position == "r":
                draw.text(((goods_price_location[0]*WR - w), goods_price_location[1] *HR), str(good_price)+moneyName, fill=hex_to_rgb(text2_color), font=font_2)
            
            #role
            if role == None:
                role_name = "없음"
            else:
                role_name = role.name
            w = draw.textlength(text=role_name, font=font_3) 
            
            if role_position == "l":
                draw.text((role_location[0]*WR, role_location[1] *HR), role_name, fill=hex_to_rgb(text3_color), font=font_3)
            elif role_position == "m":
                draw.text(((role_location[0]*WR - w/2), role_location[1] *HR), role_name, fill=hex_to_rgb(text3_color), font=font_3)
            elif role_position == "r":
                draw.text(((role_location[0]*WR - w), role_location[1] *HR), role_name, fill=hex_to_rgb(text3_color), font=font_3)

            #text
            if text_len <= 25:
                w = draw.textlength(text=text, font=font_4) 
                
                if goods_text_position == "l":
                    draw.text((goods_text_location[0], goods_text_location[1] *HR), text, fill=hex_to_rgb(text4_color), font=font_4)
                elif goods_text_position == "m":
                    draw.text(((goods_text_location[0]*WR - w/2), goods_text_location[1] *HR), text, fill=hex_to_rgb(text4_color), font=font_4)
                elif goods_text_position == "r":
                    draw.text(((goods_text_location[0]*WR - w), goods_text_location[1] *HR), text, fill=hex_to_rgb(text4_color), font=font_4)
            else:
                w = draw.textlength(text=text[0:25], font=font_4) 
                
                text = text[0:25] + "\n" + text[25:]
                if goods_text_position == "l":
                    draw.multiline_text((goods_text_location[0], (goods_text_location[1]-50) *HR), text, fill=hex_to_rgb(text4_color), font=font_4)
                elif goods_text_position == "m":
                    draw.multiline_text(((goods_text_location[0]*WR - w/2), (goods_text_location[1]-50) *HR), text, fill=hex_to_rgb(text4_color), font=font_4, align='center')
                elif goods_text_position == "r":
                    draw.multiline_text(((goods_text_location[0]*WR - w), (goods_text_location[1]-50) *HR), text, fill=hex_to_rgb(text4_color), font=font_4, align='right')
            img.save("buy_check.png")
            await inter.author.create_dm()
            await inter.author.dm_channel.send(file=disnake.File("buy_check.png"))
        except Exception as e:
            print(e)
            embed = disnake.Embed(
                title=f"오류 발생", description=f"구매 확인서 전송이 실패하였습니다.\n권한 문제이거나 오류일 수 있습니다.\n오류 코드: 구매8", color=0xFFB9B9)
            await inter.followup.send(embed=embed)
        if logchannel != 0 and type(logchannel) == int:
            try:
                await bot.get_channel(logchannel).send(file=disnake.File("buy_check.png"))
            except:
                embed = disnake.Embed(
                    title=f"오류 발생", description=f"로그채널에 구매 확인서 전송이 실패하였습니다.\n오류가 계속 될 경우 문의를 해주시기 바랍니다.\n오류 코드: 구매9", color=0xFFB9B9)
                await inter.followup.send(embed=embed)




@goods.sub_command(name="목록", description="서버에 있는 상품을 확인합니다")
async def list(inter: disnake.ApplicationCommandInteraction):
    await inter.response.defer()
    try:
        with open(f'guild/{inter.guild.id}.json', encoding="utf-8") as f:
            json_object = json.load(f)
    except:
        embed = disnake.Embed(
        title=f"사용 불가", description=f"해당 서버는 이용 동의를 하지 않았습니다.\n동의를 완료한 서버에서 해당 메세지가 계속 나올 경우 문의를 해주시기 바랍니다.", color=0xFFB9B9)
        await inter.followup.send(embed=embed)
        return
    try:
        with open(f'guild/{inter.guild.id}.json', encoding="utf-8") as f:
            json_object = json.load(f)
            goods = json_object["goods"]
            package = json_object['custom']['package']
            title_color = json_object["custom"]["color2"]
            text1_color = json_object["custom"]["color3"]
            text2_color = json_object["custom"]["color4"]
            text3_color = json_object["custom"]["color5"]
            text4_color = json_object["custom"]["color6"]
            moneyName = json_object["setting"]["moneyName"]
            if goods == {}:
                embed = disnake.Embed(
                title=f"상품이 존재하지 않습니다.", description=f"`/상품관리 추가`으로 상품을 추가해 보세요", color=0xFFB9B9)
                await inter.followup.send(embed=embed)
                return

    except:
        embed = disnake.Embed(
        title=f"오류 발생", description=f"데이터를 불러오는 과정에서 오류가 발생하였습니다.\n오류 코드: 목록1", color=0xFFB9B9)
        await inter.followup.send(embed=embed)
        return

    if package != "": #패키지
        try:
            with open(f'package/{package}.json', encoding="utf-8") as f:
                json_object = json.load(f)
                title_location = json_object["list"]["location1"]
                title_position = json_object["list"]["location1_position"]
                goods_name_location = json_object["list"]["location2"]
                goods_name_position = json_object["list"]["location2_position"]
                goods_description_location = json_object["list"]["location3"]
                goods_description_position = json_object["list"]["location3_position"]
                goods_price_location = json_object["list"]["location4"]
                goods_price_position = json_object["list"]["location4_position"]
                goods_remain_location = json_object["list"]["location5"]
                goods_remain_position = json_object["list"]["location5_position"]
                title_font = json_object["list"]["font1"] #title
                title_font_size = json_object["list"]["font_size1"]
                title_color = json_object["list"]["color1"]
                text1_font = json_object["list"]["font2"] #name
                text1_font_size = json_object["list"]["font_size2"]
                text1_color = json_object["list"]["color2"]
                text2_font = json_object["list"]["font4"] #description
                text2_font_size = json_object["list"]["font_size4"]
                text2_color = json_object["list"]["color4"]
                text3_font = json_object["list"]["font4"] #price
                text3_font_size = json_object["list"]["font_size3"]
                text3_color = json_object["list"]["color3"]
                text4_font = json_object["list"]["font3"] #remain
                text4_font_size = json_object["list"]["font_size4"]
                text4_color = json_object["list"]["color4"]
                next = json_object["list"]["next"]

        except:
            embed = disnake.Embed(
            title=f"오류 발생", description=f"패키지 형식을 불러오는데 오류가 발생하였습니다.\n문의해 주시기 바랍니다.\n오류 코드: 목록2", color=0xFFB9B9)
            await inter.followup.send(embed=embed)
            return

        try:
            img = Image.open(f"package/목록{package}.png")
            W, H = (img.width, img.height)
        except:
            embed = disnake.Embed(
                title=f"오류 발생", description=f"패키지의 이미지를 불러오지 못했습니다.\n오류가 계속 될 경우 문의해 주세요.\n오류 코드: 목록3", color=0xFFB9B9)
            await inter.followup.send(embed=embed)
            return
    else: #기본&커스텀
        try:
            with open('package/nomal.json', encoding="utf-8") as f:
                json_object = json.load(f)
                title_location = json_object["list"]["location1"]
                title_position = json_object["list"]["location1_position"]
                goods_name_location = json_object["list"]["location2"]
                goods_name_position = json_object["list"]["location2_position"]
                goods_description_location = json_object["list"]["location3"]
                goods_description_position = json_object["list"]["location3_position"]
                goods_price_location = json_object["list"]["location4"]
                goods_price_position = json_object["list"]["location4_position"]
                goods_remain_location = json_object["list"]["location5"]
                goods_remain_position = json_object["list"]["location5_position"]
                title_font = json_object["list"]["font1"] #title
                title_font_size = json_object["list"]["font_size1"]
                if "" == title_color :
                    title_color = json_object["list"]["color1"]
                text1_font = json_object["list"]["font2"] #name
                text1_font_size = json_object["list"]["font_size2"]
                if "" == text1_color :
                    text1_color = json_object["list"]["color2"]
                text2_font = json_object["list"]["font4"] #description
                text2_font_size = json_object["list"]["font_size4"]
                if "" == text2_color :
                    text2_color = json_object["list"]["color4"]
                text3_font = json_object["list"]["font3"] #price
                text3_font_size = json_object["list"]["font_size3"]
                if "" == text3_color :
                    text3_color = json_object["list"]["color3"]
                text4_font = json_object["list"]["font4"] #remain
                text4_font_size = json_object["list"]["font_size4"]
                if "" == text4_color :
                    text4_color = json_object["list"]["color4"]
                next = json_object["list"]["next"]

        except:
            embed = disnake.Embed(
                title=f"오류 발생", description=f"기본 형식을 불러오는데 오류가 발생하였습니다.\n문의해 주시기 바랍니다.\n오류 코드: 목록4", color=0xFFB9B9)
            await inter.followup.send(embed=embed)
            return

        try:
            img = Image.open(f"custom/목록{inter.guild.id}.png")
        except:
            img = Image.open("DISTORE_list.png")

        W, H = (img.width, img.height)

        if package == "":
            WR = W/2000
            HR = H/3000
            print("목록배율:" + str(WR) + "," + str(HR))
            title_len = len(inter.guild.name) 
            font_title = ImageFont.truetype(title_font, int(title_font_size*WR+15-title_len))
            font_1 = ImageFont.truetype(text1_font, int(text1_font_size*WR))
            font_2 = ImageFont.truetype(text2_font, int(text2_font_size*WR))
            font_3 = ImageFont.truetype(text3_font, int(text3_font_size*WR))
            font_4 = ImageFont.truetype(text4_font, int(text4_font_size*WR))
        else:
            WR = 1
            HR = 1

    draw = ImageDraw.Draw(img)

    #title text

    w = draw.textlength(text=inter.guild.name, font=font_title) 

    if title_position == "l":
        draw.text((title_location[0], title_location[1] *HR), inter.guild.name, fill=hex_to_rgb(title_color), font=font_title)
    elif title_position == "m":
        draw.text(((title_location[0]*WR - w/2), title_location[1] *HR), inter.guild.name, fill=hex_to_rgb(title_color), font=font_title)
    elif title_position == "r":
        draw.text(((title_location[0]*WR - w), title_location[1] *HR), inter.guild.name, fill=hex_to_rgb(title_color), font=font_title)
    count = 0
    page = 1
    for i in goods:
        description = None
        remain = 10001


        description = goods[i]['description']
        if description == "없음":
            description = None
        remain = goods[i]['remain']
        if remain == "무한":
            remain = 10001


        if count == 10: #다음 페이지
            img.save("list.png")
            await inter.followup.send(file=disnake.File("list.png"))
            page += 1

            if package == "":
                try:
                    img = Image.open(f"custom/목록{inter.guild.id}.png")
                except:
                    img = Image.open("DISTORE_list.png")
            else:
                img = Image.open("package/목록{package}.png")
            draw = ImageDraw.Draw(img)

            w = draw.textlength(text=inter.guild.name, font=font_title)

            if title_position == "l":
                draw.text((title_location[0] *WR, title_location[1] *HR), inter.guild.name, fill=hex_to_rgb(title_color), font=font_title)
            elif title_position == "m":
                draw.text(((title_location[0]*WR - w/2), title_location[1] *HR), inter.guild.name, fill=hex_to_rgb(title_color), font=font_title)
            elif title_position == "r":
                draw.text(((title_location[0]*WR - w), title_location[1] *HR), inter.guild.name, fill=hex_to_rgb(title_color), font=font_title)
            count = 0

        #name

        w = draw.textlength(text=i, font=font_1)

        if goods_name_position == "l": 
            draw.text((goods_name_location[0] *WR, goods_name_location[1]*HR + next*HR*count), i, fill=hex_to_rgb(text1_color), font=font_1)
        elif goods_name_position == "m":
            draw.text(((goods_name_location[0]*WR - w/2), goods_name_location[1]*HR + next*HR*count), i, fill=hex_to_rgb(text1_color), font=font_1)
        elif goods_name_position == "r":
            draw.text(((goods_name_location[0]*WR - w), goods_name_location[1]*HR + next*HR*count), i, fill=hex_to_rgb(text1_color), font=font_1)
        
        #description

        if description != None:
            w = draw.textlength(text=description, font=font_2)

            if goods_description_position == "l": 
                draw.text((goods_description_location[0] *WR, goods_description_location[1]*HR + next*HR*count), description, fill=hex_to_rgb(text2_color), font=font_2)
            elif goods_description_position == "m":
                draw.text(((goods_description_location[0]*WR - w/2), goods_description_location[1] *HR), description, fill=hex_to_rgb(text2_color), font=font_2)
            elif goods_description_position == "r":
                draw.text(((goods_description_location[0]*WR - w), goods_description_location[1]*HR + next*HR*count), description, fill=hex_to_rgb(text2_color), font=font_2)

        #price

        w = draw.textlength(text=str(goods[i]['good_price'])+" "+str(moneyName), font=font_3)

        if goods_price_position == "l": 
            draw.text((goods_price_location[0] *WR, goods_price_location[1]*HR + next*HR*count), str(goods[i]['good_price'])+" "+str(moneyName), fill=hex_to_rgb(text3_color), font=font_3)
        elif goods_price_position == "m":
            draw.text(((goods_price_location[0]*WR - w/2), goods_description_location[1] *HR), str(goods[i]['good_price'])+" "+str(moneyName), fill=hex_to_rgb(text3_color), font=font_3)
        elif goods_price_position == "r":
            draw.text(((goods_price_location[0]*WR - w), goods_price_location[1]*HR + next*HR*count), str(goods[i]['good_price'])+" "+str(moneyName), fill=hex_to_rgb(text3_color), font=font_3)
        
        #remain
        
        if int(remain) > 10000:
            remain = "무한"
        w = draw.textlength(text=f"재고 : {remain}개", font=font_4)

        if goods_remain_position == "l": 
            draw.text((goods_remain_location[0] *WR, goods_remain_location[1]*HR + next*HR*count), f"재고 : {remain}개", fill=hex_to_rgb(text4_color), font=font_4)
        elif goods_remain_position == "m":
            draw.text(((goods_remain_location[0]*WR - w/2), goods_description_location[1] *HR), f"재고 : {remain}개", fill=hex_to_rgb(text3_color), font=font_4)
        elif goods_remain_position == "r":
            draw.text(((goods_remain_location[0]*WR - w), goods_remain_location[1]*HR + next*HR*count), f"재고 : {remain}개", fill=hex_to_rgb(text4_color), font=font_4)
        
        count += 1

    img.save("list.png")
    await inter.followup.send(file=disnake.File("list.png"))

async def autocomp_goods(inter: disnake.ApplicationCommandInteraction, user_input: str):
    try:
        with open(f'guild/{inter.guild.id}.json', encoding="utf-8") as f:
            json_object = json.load(f)
            goods = json_object["goods"]
    except:
        goods = []
    return [good for good in goods if user_input in good]

@goods.sub_command(name="정보", description="상품의 정보를 확인합니다.")
async def list(inter: disnake.ApplicationCommandInteraction, 상품: str = commands.Param(autocomplete=autocomp_goods)):
    await inter.response.defer()
    if inter.author.guild_permissions.administrator:
        try:
            with open(f'guild/{inter.guild.id}.json', encoding="utf-8") as f:
                json_object = json.load(f)
                price = json_object["goods"][str(상품)]["good_price"]
                description = json_object["goods"][str(상품)]["description"]
                remain = json_object["goods"][str(상품)]["remain"]
                time = json_object["goods"][str(상품)]["time"]
                goodcount = json_object["goods"][str(상품)]["goodcount"]
                text = json_object["goods"][str(상품)]["text"]
                roleId = json_object["goods"][str(상품)]["roleId"]
                moneyName = json_object["setting"]["moneyName"]
        except:
            embed = disnake.Embed(
            title=f"오류 발생", description=f"데이터를 불러오는 과정에서 오류가 발생하였습니다.\n오류 코드: 정보1", color=0xFFB9B9)
            await inter.followup.send(embed=embed)
            return
        if roleId != "`없음`" and type(roleId) == int:
            roleId = disnake.utils.get(inter.guild.roles, id=roleId).mention
        embed = disnake.Embed(
            title=f"{상품} 정보", description=f"가격 : `{price}`{moneyName}", color=0xFFB9B9)
        embed.add_field(
            name=f"설명", value=f"`{description}`", inline=False)
        embed.add_field(
            name=f"재고", value=f"`{remain}`개", inline=False)
        embed.add_field(
            name=f"지급 역할", value=f"{roleId}", inline=False)
        embed.add_field(
            name=f"지급 텍스트", value=f"{text}", inline=False)
        embed.add_field(
            name=f"추가일", value=f"{time}", inline=False)
        embed.add_field(
            name=f"구매 횟수", value=f"{goodcount}", inline=False)
        await inter.followup.send(embed=embed)
    else:
        try:
            with open(f'guild/{inter.guild.id}.json', encoding="utf-8") as f:
                json_object = json.load(f)
                price = json_object["goods"][str(상품)]["good_price"]
                description = json_object["goods"][str(상품)]["description"]
                remain = json_object["goods"][str(상품)]["remain"]
                moneyName = json_object["setting"]["moneyName"]
                time = json_object["goods"][str(상품)]["time"]
        except:
            embed = disnake.Embed(
            title=f"오류 발생", description=f"데이터를 불러오는 과정에서 오류가 발생하였습니다.\n오류 코드: 정보2", color=0xFFB9B9)
            await inter.followup.send(embed=embed)
            return
        embed = disnake.Embed(
            title=f"{상품} 정보", description=f"가격 : `{price}`{moneyName}", color=0xFFB9B9)
        embed.add_field(
            name=f"설명", value=f"`{description}`", inline=False)
        embed.add_field(
            name=f"재고", value=f"`{remain}`개", inline=False)
        embed.add_field(
            name=f"추가일", value=f"{time}", inline=False)
        await inter.followup.send(embed=embed) 

rank = commands.option_enum(["채팅", "음성채팅", "출석", "활동", "돈"])

@bot.slash_command(name="랭크", description="서버 유저들의 랭킹을 알려줍니다.")
async def rank(inter: disnake.ApplicationCommandInteraction, value: rank):
    await inter.response.defer()
    try:
        with open(f'guild/{inter.guild.id}.json', encoding="utf-8") as f:
            json_object = json.load(f)
    except:
        embed = disnake.Embed(
        title=f"사용 불가", description=f"해당 서버는 이용 동의를 하지 않았습니다.\n동의를 완료한 서버에서 해당 메세지가 계속 나올 경우 문의를 해주시기 바랍니다.", color=0xFFB9B9)
        await inter.followup.send(embed=embed)
        return
    if value == "채팅":
        value = "chat"
    elif value == "음성채팅":
        value = "voice"
    elif value == "출석":
        value = "attendance"
    elif value == "활동":
        value = "activity"
    elif value == "돈":
        value = "money"
    try:
        with open(f'guild/{inter.guild.id}.json', encoding="utf-8") as f:
            json_object = json.load(f)
            rank_user = sorted(json_object["user"].items(), key=lambda item: item[1][value], reverse=True)
    except:
        embed = disnake.Embed(
        title=f"오류 발생", description=f"데이터를 불러오는 과정에서 오류가 발생하였습니다.\n오류 코드: 랭크1", color=0xFFB9B9)
        await inter.followup.send(embed=embed)
        return
    rank_list = ""
    count = 0
    for i in rank_user:
        count += 1
        rank_list += f"\n`{str(count).rjust(2, '0')}` <@{i[0]}>: `{i[1][value]}`"
        if count >= 50:
            break
    embed = disnake.Embed(
    title=f"{value} 랭크", description=f"1~50등의 유저들을 보여줍니다{rank_list}", color=0xFFB9B9)
    await inter.followup.send(embed=embed)



@bot.slash_command(name="출석", description="매일 한번 돈을 받습니다")
async def attendance(inter: disnake.ApplicationCommandInteraction):
    await inter.response.defer()
    try:
        with open(f'guild/{inter.guild.id}.json', encoding="utf-8") as f:
            json_object = json.load(f)
    except:
        embed = disnake.Embed(
        title=f"사용 불가", description=f"해당 서버는 이용 동의를 하지 않았습니다.\n동의를 완료한 서버에서 해당 메세지가 계속 나올 경우 문의를 해주시기 바랍니다.", color=0xFFB9B9)
        await inter.followup.send(embed=embed)
        return
    try:
        with open(f'guild/{inter.guild.id}.json', encoding="utf-8") as f:
            json_object = json.load(f)
            attendance = json_object["setting"]["attendance"]
            moneyName = json_object["setting"]["moneyName"]
            day = json_object["user"][str(inter.author.id)]["day"]
    except:
        embed = disnake.Embed(
        title=f"오류 발생", description=f"데이터를 불러오는 과정에서 오류가 발생하였습니다.\n오류 코드: 출석1", color=0xFFB9B9)
        await inter.followup.send(embed=embed)
        return
    if day != None:
        day = int(day)
    else :
        day = 0
    today = int(time.localtime(time.time()).tm_mday) + int(time.localtime(time.time()).tm_mon)*100
    if today != day :
        json_object["user"][str(inter.author.id)]["day"] = today
        json_object["user"][str(inter.author.id)]["money"] += attendance
        try:
            json_object["user"][str(inter.author.id)]["attendance"] += 1
        except:
            json_object["user"][str(inter.author.id)]["attendance"] = 1
        money = json_object["user"][str(inter.author.id)]["money"]
        if moneyName == None:
            moneyName = "원"
        embed = disnake.Embed(
            title=f"출석", description=f"출석으로 `{attendance}`{moneyName}을 받았습니다.\n현재 보유금 : `{money}`{moneyName}", color=0xFFB9B9)
        try:
            with open(f'guild/{inter.guild.id}.json', 'w', encoding="utf-8") as f:
                json.dump(json_object, f, indent=2, ensure_ascii=False)
        except:
            embed = disnake.Embed(
            title=f"오류 발생", description=f"데이터를 저장하는 과정에서 오류가 발생하였습니다.\n오류가 계속 될 경우 문의를 해주시기 바랍니다.\n오류 코드: 출석2", color=0xFFB9B9)
            await inter.followup.send(embed=embed)
            return
    else:
        embed = disnake.Embed(
            title=f"출석", description=f"이미 출석을 하셨습니다\n다음날 다시 시도 해주세요", color=0xFFB9B9)
    await inter.followup.send(embed=embed)



@bot.slash_command(name="dev")
async def dev(inter):
    pass

@dev.sub_command(name="send", description="do not use this command")
async def server(inter, channel: str, message: str):
    if inter.author.id == 731713372990603296:
        await inter.response.defer()
        await bot.get_channel(int(channel)).send(message)
        await inter.followup.send("전송 완료")



unit = commands.option_enum(["초", "분", "시간", "일", "월", "년"])

@dev.sub_command(name="premium", description="do not use this command")
async def server(inter: disnake.ApplicationCommandInteraction, server: str, add: int, unit: unit):
    if inter.author.id == 731713372990603296:
        await inter.response.defer(ephemeral=True)
        try:
            with open(f'guild/{server}.json', encoding="utf-8") as f:
                json_object = json.load(f)
                expiration_date = json_object["premium"]["expiration_date"]
        except:
            embed = disnake.Embed(
            title=f"오류 발생", description=f"데이터를 불러오는 과정에서 오류가 발생하였습니다.", color=0xFFB9B9)
            await inter.followup.send(embed=embed)
            return
        if unit == '분':
            add *= 60
        elif unit == "시간":
            add *= 60
            add *= 60
        elif unit == "일":
            add *= 60
            add *= 60
            add *= 24
        elif unit == "월":
            add *= 60
            add *= 60
            add *= 24
            add *= 30
        elif unit == "년":
            add *= 60
            add *= 60
            add *= 24
            add *= 365
        if expiration_date == 0:
            expiration_date = int(time.time()) + add
        elif  expiration_date>time.time():
            expiration_date += add
        else:
            expiration_date = int(time.time()) + add
        try:
            json_object["premium"]["expiration_date"] = expiration_date
            with open(f'guild/{server}.json', 'w', encoding="utf-8") as f:
                json.dump(json_object, f, indent=2, ensure_ascii=False)
        except:
            embed = disnake.Embed(
            title=f"오류 발생", description=f"데이터를 저장하는 과정에서 오류가 발생하였습니다.\n오류가 계속 될 경우 문의를 해주시기 바랍니다.", color=0xFFB9B9)
            await inter.followup.send(embed=embed)
            return
        await inter.followup.send(f"만료일: <t:{expiration_date}>")







bot.run("TOKEN")  # Replace TOKEN with your bot's token