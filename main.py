from Yachu import *
import discord
import asyncio
from discord.ext import commands


token = open('data/token.txt','r').readline()
game = discord.Game("야추")
bot = commands.Bot(command_prefix='!',activity = game)
playerID = None



@bot.event
async def on_ready():
    await bot.guilds[0].channels[2].send("bot started")

@bot.command(name='야추시작')
async def start(ctx):
    global playerID
    if playerID == None:
        await ctx.send(f'{ctx.author.mention}님과 야추를 시작합니다')
        playerID = ctx.author.id
        await playing(ctx)
    elif playerID == ctx.author.id: pass
    else: await ctx.send("다른 분과 이미 야추중이에요. 기다려주세요")

@bot.command(name='야추그만')
async def end(ctx):
    global playerID
    if ctx.author.id == playerID:
        await ctx.send(f'{ctx.author.mention}님, 즐거운 야추였어요!')
        playerID = None
    else: await ctx.send(f'네? 저는 {ctx.author.mention}님과 야추한적이 없는데요?')

@bot.command(name='야추도움')
async def help(ctx):
    await ctx.send('!야추시작 - 야추봇과 야추 주사위 연습게임을 시작합니다.\n'
                   '!야추그만 - 게임을 중도 포기합니다.\n'
                   '!야추도움 - 이 도움말을 봅니다.\n'
                   '!야추베팅 - 날갱점수를 걸고 총점 200점에 도전합니다.(추가예정)\n'
                   '!야추대결 - 날갱점수를 걸고 상대와 대결합니다.(추가예정)'
                   )

@bot.command(name='야추베팅')
async def bet(ctx):
    pass

@bot.command(name='야추대결')
async def vs(ctx):
    pass



async def playing(ctx):
    yachu = Yachu()
    def author_check(m):
        if m.author.id != playerID: return False
        return True
    i = 12
    while i > 0:
        while yachu.phase < 3:
            await ctx.channel.send(embed = yachu.getScoreBoardDiscord())
            await ctx.channel.send(yachu.rollDice())

            if yachu.phase == 3:
                await ctx.channel.send("저장할 칸을 선택해주세요")
                counter = 6
                while counter > 0:
                    if counter == 1:
                        await ctx.channel.send('너 인성에 문제있어?')
                        await end(ctx)
                        return
                    msg = await bot.wait_for('message',check=author_check)
                    try:
                        if msg.content.startswith('!야추그만'): return
                        ind = int(msg.content)
                        if yachu.isAvailable(ind):break
                        else:
                            await ctx.channel.send('잘못된 입력입니다. 다시 말씀해주세요')
                            continue
                    except:
                        await ctx.channel.send('잘못된 입력입니다. 다시 말씀해주세요')
                        counter -=1
                        continue


            else:
                await ctx.channel.send("저장할 칸 선택, 다시굴리려면 0")
                counter = 6
                while counter>0:
                    if counter == 1:
                        await ctx.channel.send('너 인성에 문제있어?')
                        await end(ctx)
                        return
                    msg = await bot.wait_for('message',check=author_check)
                    try:
                        if msg.content.startswith('!야추그만'): return
                        ind = int(msg.content)
                        if yachu.isAvailable(ind) or ind == 0 : counter = 0
                        else:
                            await ctx.channel.send('잘못된 입력입니다. 다시 말씀해주세요')
                            continue
                    except:
                        await ctx.channel.send('잘못된 입력입니다. 다시 말씀해주세요')
                        counter -= 1
                        continue

            if ind == 0:
                yachu.unlockAll()
                await ctx.channel.send('고정할 주사위 선택 - ex) 1 2 4, 없으면 0')
                counter = 6
                while counter>0:
                    if counter == 1:
                        await ctx.channel.send('너 인성에 문제있어?')
                        await end(ctx)
                        return
                    msg = await bot.wait_for('message',check=author_check)
                    try:
                        if msg.content.startswith('!야추그만'): return
                        temp = msg.content.split()
                        if len(temp) == 1 and temp[0] == '0': counter = 0
                        for ind in temp:
                            ind = int(ind)
                            yachu.lock(ind)
                        counter = 0

                    except:
                        await ctx.channel.send('잘못된 입력입니다. 다시 말씀해주세요')
                        counter -= 1
                        continue


            else:
                yachu.setScore(ind)
                break
        i -=1
    await ctx.channel.send(embed=yachu.getScoreBoardDiscord())
    await ctx.channel.send('축하합니다!{}점을 얻으셨습니다!'.format(yachu.score[14]))



bot.run(token)
