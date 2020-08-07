from Yachu import *
import discord
from discord.ext import commands
from ext_nalgang import *


class ReAsk(Exception):
    pass


token = open('data/token.txt', 'r').readline()
game = discord.Game("도움말은 !야추도움")
bot = commands.Bot(command_prefix='!', activity=game)
playerID = []


@bot.event
async def on_ready():
    print("bot started")


@bot.command(name='야추시작')
async def start(ctx):
    global playerID
    if len(playerID) == 0:
        await ctx.send(f'{ctx.author.mention}님과 야추를 시작합니다')
        playerID.append(ctx.author.id)
        await playing(ctx, 0)
    elif ctx.author.id in playerID:
        return
    else:
        await ctx.send("다른 분과 이미 야추중이에요. 기다려주세요")
        return


@bot.command(name='야추그만')
async def end(ctx):
    global playerID
    if ctx.author.id in playerID:
        await ctx.send(f'{ctx.author.mention}님, 즐거운 야추였어요!')
        playerID = []
    else:
        await ctx.send(f'네? 저는 {ctx.author.mention}님과 야추한적이 없는데요?')


# 자주 쓰는 함수들
def author_check(m):
    if m.author.id in playerID: return True
    return False


async def question(ctx, dia, func):
    await ctx.send(dia)
    counter = 6
    while counter > 0:
        if counter == 1:
            await ctx.send('너 인성에 문제있어?')
            await end(ctx)
            return -1
        msg = await bot.wait_for('message', check=author_check)
        try:
            if msg.content.startswith('!야추그만'): return -1
            return func(msg)
        except:
            await ctx.send('잘못된 입력입니다. 다시 말씀해주세요')
            counter -= 1
            continue


@bot.command(name='야추도움')
async def help(ctx):
    await ctx.send('!야추시작 - 야추봇과 야추 주사위 연습게임을 시작합니다.\n'
                   '!야추그만 - 게임을 중도 포기합니다. 야추봇과의 대화가 즉시 종료됩니다.\n'
                   '!야추도움 - 이 도움말을 봅니다.\n'
                   '!야추베팅 - 날갱점수를 걸고 총점 200점에 도전합니다.\n'
                   '!야추대결 - 날갱점수를 걸고 상대와 대결합니다.(추가예정)'
                   )


@bot.command(name='야추베팅')
async def bet(ctx):
    global playerID
    if len(playerID) == 0:
        await ctx.send(f'{ctx.author.mention}님이 날갱점수를 걸고 야추 200점에 도전합니다.')
        playerID.append(ctx.author.id)
    elif ctx.author.id in playerID:
        return
    else:
        await ctx.send("다른 분과 이미 야추중이에요. 기다려주세요")
        return

    def func3(msg):
        now = ng_getpoint(ctx.author)
        betpoint = int(msg.content)
        print(betpoint)
        if betpoint > now or betpoint <= 0: raise ReAsk
        return betpoint

    betpoint = await question(ctx, f'현재 점수는 {ng_getpoint(ctx.author)}점입니다. 얼마나 거시겠어요?', func3)
    if betpoint == -1:
        await end(ctx)
        return
    await playing(ctx, betpoint)


@bot.command(name='야추대결')
async def vs(ctx, user: discord.member.Member, point: int):
    global playerID
    if len(playerID) == 0:
        a, b = ng_getpoint(ctx.author), ng_getpoint(user)
        if a < point or b < point or point < 0:
            await ctx.send(f'거 상도덕은 지키면서 삽시다. 어떻게 {point}점을 걸겠다고 그러십니까?\n(현재 각각 {a}점, {b}점 보유)')
        else:
            playerID.append(ctx.author.id)
            playerID.append(user.id)
            await ctx.send(f'{ctx.author.mention}님이 {user.mention}님과 {point}점을 걸고 대결을 신청합니다.')
            await ctx.send(f'{user.display_name}님, 동의하시면 1분 내에 \"나는야 야추왕\"이라고 정확히 적어주세요')

            def check(m):
                if user.id != m.author.id: return False
                if m.content != '나는야 야추왕': return False
                return True

            try:
                await bot.wait_for('message', check=check, timeout=60)
            except TimeoutError:
                await ctx.send('도전 거절!')
                playerID = []
                return
            await ctx.send(f'{ctx.author.display_name}님과 {user.display_name}님의 대결이 시작됩니다!')
            await vs_playing(ctx, user, point)

    elif ctx.author in playerID:
        return

    else:
        await ctx.send("다른 분과 이미 야추중이에요. 기다려주세요")
        return


async def playing(ctx, betpoint):
    ng_addpoint(ctx.author, -1 * betpoint)
    yachu = Yachu()
    i = 12
    while i > 0:
        while yachu.phase < 3:
            await ctx.send(embed=yachu.getScoreBoardDiscord())
            await ctx.send(yachu.rollDice())
            if yachu.phase == 3:

                def func1(msg):
                    this = int(msg.content)
                    if yachu.isAvailable(this):
                        return this
                    else:
                        raise ReAsk

                ind = await question(ctx, '저장할 칸 선택', func1)

            else:
                def func2(msg):
                    this = int(msg.content)
                    if this == 0: return this
                    if yachu.isAvailable(this):
                        return this
                    else:
                        raise ReAsk

                ind = await question(ctx, '저장할 칸 선택, 다시 굴리려면 0', func2)

            if ind == -1: return
            if ind == 0:
                yachu.unlockAll()

                def func3(msg):
                    temp = msg.content.split()
                    if len(temp) == 1 and temp[0] == '0': return
                    for ind in temp:
                        ind = int(ind)
                        yachu.lock(ind)
                    return

                if await question(ctx, '고정할 주사위 선택 - ex) 1 2 4, 없으면 0', func3) == -1: return

            else:
                yachu.setScore(ind)
                break
        i -= 1
    await ctx.send(embed=yachu.getScoreBoardDiscord())
    await ctx.send('{}점을 얻으셨습니다!'.format(yachu.score[14]))
    if betpoint > 0:
        if yachu.score[14] < 200:
            await ctx.send('안타깝게도 200점을 획득하지는 못하셨네요. 다음 기회에!')
        else:
            ng_addpoint(ctx.author, 2 * betpoint)
            await ctx.send(f'200점 이상을 획득하셨네요. {betpoint}점을 획득하여 현재 날갱 점수는{ng_getpoint(ctx.author)}입니다!')
    await end(ctx)
    return


async def vs_playing(ctx, user, betpoint):
    return


bot.run(token)
