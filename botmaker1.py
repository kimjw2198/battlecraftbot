import discord
import asyncio
import random
import openpyxl
import requests
from json import loads
from discord.ext import commands
from discord.ext.commands import bot

client = discord.Client()
app = discord.Client()
bot = commands.Bot(command_prefix='/')

token = 'Njg5MDQwMTg5NDY0NjQxNjM1.XnASGQ.eA_cO4HnL_K9AswCHooGYzhF2TE'

@client.event
async def on_ready():
    print('다음으로 로그인 합니다 : ')
    print(client.user.name)
    print('connection was successful')
    game = discord.Game('배틀크래프트')
    await client.change_presence(status=discord.Status.online, activity=game)
    twitch = "battlecraft1234"
    name = "배틀크래프트"
    channel = client.get_channel(686112424423587850)
    a = 0
    while True:
        headers = {'Client-ID' : 'jr8kj49tkykgocq7rq4mvait9hg7gd'}
        response = requests.get("https://api.twitch.tv/helix/streams?user_login=" + twitch, headers=headers)
        try:
            if loads(response.text)['data'][0]['type'] == 'live' and a == 0:
                await channel.send(name = "님이 방송을 시작하셨습니다.")
                a = 1
        except:
            a = 0
        await asyncio.sleep(10)


@client.event
async def on_message(message):
    if message.author.bot:
        return None
    if (message.content == 'ㅎㅇ'):
        await message.channel.send('ㅎㅇ')

    if message.content.startswith("/사진"):
        pic = message.content.split(" ")[1]
        await message.channel.send(file=discord.File(pic))

    if message.content.startswith("/공지"):
        channel = message.content[7:25]
        msg = message.content[26:]
        embed = discord.Embed(colour = 660099)
        embed.add_field(name='채널메시지', value= (msg), inline=False)
        await client.get_channel(int(channel)).send(embed=embed)

    if message.content.startswith("/DM"):
        author =  message.guild.get_member(int(message.content[4:22]))
        msg = message.content[23:]
        embed = discord.Embed(colour = 660099)
        embed.add_field(name='개인DM', value= (msg), inline=False)
        await author.send(embed=embed)

    if message.content.startswith("/뮤트"):
        author = message.guild.get_member(int(message.content[4:22]))
        channel = message.content[23:41]
        msg = message.content[42:]
        embed = discord.Embed(colour = 660099)
        role = discord.utils.get(message.guild.roles, name="뮤트중")
        embed.add_field(name='뮤트', value= (msg), inline=False)
        await author.add_roles(role)
        await channel.send(embed=embed)

    if message.content.startswith("/언뮤트"):
        author = message.guild.get_member(int(message.content[5:23]))
        role = discord.utils.get(message.guild.roles, name="뮤트중")
        await author.remove_roles(role)

    if message.content.startswith("/경고"):
        author = message.guild.get_member(int(message.content[4:22]))
        file = openpyxl.load_workbook("경고.xlsx")
        sheet = file.active
        i = 1
        while True:
            if sheet["A" + str(i)].value == str(author.id):
                    sheet["A" + str(i)].value = int(sheet["B" + str(i)].value) + 1
                    file.save("경고.xlsx")
                    if sheet ["B" + str(i)].value == 3:
                        await message.guild.ban(author)
                        await message.channel.send("경고 3회 누적입니다. 서버에서 추방됩니다.")
                    else:
                        await message.channel.send("경고를 1회 받았습니다.")
                    break
                
            if sheet["A" + str(i)].value == None:
                sheet["A" + str(i)].value = str(author.id)
                sheet["B" + str(i)].value = 1
                file.save("경고.xlsx")
                await message.channel.send("경고를 1회 받았습니다.")
                break
                i += 1

    if message.content.startswith("") and message.author.id!= 689040189464641635:
        file = openpyxl.load_workbook("레벨.xlsx")
        sheet = file.active
        exp = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000]
        i = 1
        while True:
            if sheet["A" + str(i)].value == str(message.author.id):
                sheet["B" + str(i)].value = sheet["B" + str(i)].value + 1
                if sheet["B" + str(i)].value >= exp[sheet["C" + str(i)].value - 1]:
                        sheet["C" + str(i)].value = sheet["C" + str(i)].value + 1
                        await message.channel.send("레벨이 올랐습니다. \n현재 레벨 : " + str(sheet["C" + str(i)].value) + "\n경험치 : " + str(sheet["B" + str(i)].value))
                        file.save("레벨.xlsx")
                        break
                    
    
            if sheet["A" + str(i)].value == None:
                sheet["A" + str(i)].value = str(message.author.id)
                sheet["B" + str(i)].value = 0
                sheet["C" + str(i)].value = 1
                file.save("레벨.xlsx")
                break

            i += 1

    if message.content.startswith('/주사위'):
        roll = message.content.split(" ")
        rolld = roll[1].split("d")
        dice = 0
        for i in range(1, int(rolld[0])+1):
            dice = dice + random.randint(1, int(rolld[1]))
        await client.send_message(message.channel, str(dice))

    if message.content.startswith("/뭐먹지"):
        food = "짜장면 짬뽕 치킨 라면 밥 피자 김치찌개 탕수육 수육 족발"
        foodchoice = food.split(" ")
        foodnumber = random.randint(1, len(foodchoice))
        foodresult = foodchoice[foodnumber-1]
        await client.send_message(message.channel, foodresult)

    if message.content.startswith("/서버목록불러오기"):
        list = []
        for server in client.servers:
            list.append(server.name)
        await client.send_message(message.channel, "\n".join(list))

    if message.content.startswith("/시간"):
        a = datetime.datetime.today().year
        b = datetime.datetime.today().month
        c = datetime.datetime.today().day
        d = datetime.datetime.today().hour
        e = datetime.datetime.today().minute
        f = datetime.datetime.today().second
        await client.send_message(message.channel, )

@app.command(name="추방", pass_context=True)
async def _kick(ctx, *, user_name: discord.Member, reason=None):
    await user_name.kick(reason=reason)
    await ctx.send(str(user_name)+"을(를) 추방하였습니다.")
    
        
            


client.run('Njg5MDQwMTg5NDY0NjQxNjM1.XnASGQ.eA_cO4HnL_K9AswCHooGYzhF2TE')
