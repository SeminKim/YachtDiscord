from Yachu import *
import discord
import asyncio
from discord.ext import commands


token = open('data/token.txt','r').readline()
game = discord.Game("야추")
bot = commands.Bot(command_prefix='!',activity = game)
master = None


@bot.event
async def on_ready():
    print("bot started")

@bot.command(name='야추시작')
async def start(ctx):
    await ctx.send(ctx.author.mention+"님과 야추를 시작합니다")
    await playing(ctx)

@bot.command(name='야추그만')
async def end(ctx):
    await ctx.send(ctx.author.mention + "님, 즐거운 야추였어요!")


async def playing(ctx):
    master = ctx.author
    yachu = Yachu()
    def author_check(m):
        if m.author != master: return False
        return True
    '''
    def isCorrect_1(m):
        if m.author != master: return False
        try:
            num = int(m.content)
            if yachu.isAlive[num-1]: return True
            await ctx.channel.send('올바르지 않은 형식입니다.')
            return False
        except:
            await ctx.channel.send('올바르지 않은 형식입니다.')
            return False
    
    def isCorrect_2(m):
        if m.author != master: return False
        if int(m.content) ==0: return True
        try:
            num = int(m.content)
            if yachu.isAlive[num-1]: return True
            await ctx.channel.send('올바르지 않은 형식입니다.')
            return False
        except:
            await ctx.channel.send('올바르지 않은 형식입니다.')
            return False

    def isCorrect(m):
        if m.author != master: return False
    '''

    for i in range(12):
        while yachu.phase < 3:
            await ctx.channel.send(yachu.getScoreBoard())
            await ctx.channel.send(yachu.rollDice())

            if yachu.phase == 3:
                await ctx.channel.send("저장할 칸 선택")
                msg = await bot.wait_for('message',check=author_check)
                ind = int(msg.content)

            else:
                await ctx.channel.send("저장할 칸 선택, 다시굴리려면 0")
                msg = await bot.wait_for('message',check=author_check)
                ind = int(msg.content)

            if ind == 0:
                for i in range(5): yachu.unlock(i)
                await ctx.channel.send('고정할 주사위 선택 - ex) 1 2 4, 없으면 0')
                msg = await bot.wait_for('message',check=author_check)
                temp = msg.content.split()
                if int(temp[0])!=0:
                    for i in temp: yachu.lock(int(i))

            else:
                yachu.setScore(ind)
                break
    await ctx.channel.send(yachu.getScoreBoard())
    await ctx.channel.send('축하합니다!{}점을 얻으셨습니다!'.format(yachu.score[14]))



bot.run(token)

