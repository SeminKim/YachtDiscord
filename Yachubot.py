from Yachu import *
from MultiYachu import MultiYachu
from discord.ext import commands
from asyncio import TimeoutError
from ext_nalgang import *
from config import *


whitelist = CHANNEL_WHITELIST
game = discord.Game("도움말은 !야추도움")
bot = commands.Bot(command_prefix='!', activity=game)
bot.player_one = None
bot.player_two = None
bot.channel_now = None

def makefree(bot):
    bot.player_one = None
    bot.player_two = None
    bot.channel_now = None
    return

@bot.check  # only available in whitelisted channel
async def channel_whitelist(ctx):
    with open('data/log.txt', 'a') as f:
        f.write(f'{ctx.message.content} called by {ctx.author.display_name} in {ctx.channel.name} at {time.ctime()}\n')
    return ctx.channel.id in whitelist


@bot.event
async def on_ready():
    makefree(bot)
    with open('data/log.txt', 'a') as f:
        f.write(f'bot started at {time.ctime()}\n')
    for channelid in whitelist:
        #await bot.get_channel(channelid).send('야추봇이 시작되었습니다!')
        print("READY")


@bot.command(name='야추연습')
async def start(ctx:discord.ext.commands.Context):
    if bot.player_one != None:
        await ctx.send("다른 분과 이미 야추중이에요. 기다려주세요")
        return
    else:
        await ctx.send(f'{ctx.author.mention}님과 야추 연습을 시작합니다.')
        bot.player_one = ctx.author
        bot.channel_now = ctx.channel
        await single_play(ctx.author, bot.channel_now, betpoint=0)


@bot.command(name='야추도움')
async def help(ctx):
    await ctx.send('```\n'
                   '!야추도움 - 이 도움말을 봅니다.\n'
                   '!야추연습 - 야추봇과 야추 주사위 연습게임을 시작합니다.\n'
                   '!야추베팅 - 날갱점수를 걸고 총점 200점에 도전합니다. 승리하면 건 점수만큼 얹어서 돌려받습니다.\n'
                   '!야추대결 @대결상대 점수 - 날갱점수를 걸고 상대와 대결합니다.\n'
                   '!야추규칙 - 몇가지 주의사항을 확인합니다. 버그 및 점수 유실 방지를 위해 한번쯤 읽어보세요.'
                   '```'
                   )


@bot.command(name='야추규칙')
async def rule(ctx):
    await ctx.send('```\n'
                   '1. 이 봇의 소스코드는 완전히 스파게티입니다. 성능이 처참하므로 너무 빨리 입력하지 않도록 해주세요.\n'
                   '2. 주사위를 처음 굴린 후, 다시 굴리고 싶다면 먼저 0을 입력하고, 고정할 주사위의 "눈"이 아닌 "번호"를 입력해주세요.\n'
                   '3. 잘못된 입력이 여러 번 들어오면 자동으로 게임이 종료됩니다. 게임 중 채팅을 치고 싶다면 야-추가 아닌 다른 채널을 이용하여 예방할 수 있습니다.\n'
                   '4. 버그제보 및 코드 리뷰, 기능 추가는 언제든 환영입니다! => https://github.com/SeminKim/YachtDiscord\n'
                   '```'
                   )


@bot.command(name='야추베팅')
async def bet(ctx, point:int):
    if bot.player_one != None:
        await ctx.send("다른 분과 이미 야추중이에요. 기다려주세요")
        return
    if point < 0:
        await ctx.send('되겠냐고ㅋㅋㅋ')
        return
    limit = ng_getpoint(ctx.author)
    if point > limit: #생각해보니 게임 전 베팅액을 미리 차감해야할 것 같음. 게임하면서 동시에 다른 채널에서 뒤로 빼돌리는 문제가 있음
        drip_msg:discord.Message = await ctx.send(f'{limit}점 가지고 있어서 {point}점 베팅할 수 없어요. ㅋㅋㅋㅋ거지쉑')
        time.sleep(1)
        await drip_msg.edit(content=f'{limit}점 가지고 있어서 {point}점 베팅할 수 없어요ㅠ.ㅠ')
        return

    await ctx.send(f'{ctx.author.mention}님이 {point}점을 걸고 야추 200점에 도전합니다.')
    bot.player_one = ctx.author
    bot.channel_now = ctx.channel
    await single_play(ctx.author,bot.channel_now, betpoint=point)


"""@yachubot.command(name='야추대결')
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
                await yachubot.wait_for('message', check=check, timeout=60)
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
        return"""


async def single_play(player:discord.Member, chan:discord.TextChannel, betpoint=0):
    yachu = Yachu()
    i = 12
    dice_index_list = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','🆗'] #OK 뒤로 빼고 밑에 인덱스 고쳐야함
    save_index_list = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','🇦','🇧','🇨','🇩','🇪','🇫','🆗']
    def check(reaction, user):
        return user == player and str(reaction.emoji) == '🆗'

    while i > 0:
        board_msg = await chan.send(embed=yachu.getScoreBoard())
        while yachu.phase < 3:
            roll_msg = await chan.send(yachu.rollDice())
            phase_msg = await chan.send('\n{}번 다시 굴릴 수 있습니다'.format(3 - yachu.phase))
            if yachu.phase == 3: break #굴릴 기회가 없으면 저장하러 보냄
            ask_msg = await chan.send('다시 굴릴 주사위 번호를 고르고 :ok:버튼을 눌러주세요.')
            for button in dice_index_list:  #이렇게 해도 되는지 의문?? 일단 넘어감
                await ask_msg.add_reaction(button)

            try:
                reaction_type, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
            except TimeoutError:
                await chan.send('Timeout!')
                await ng_addpoint(chan,player,-1 * betpoint)
                makefree(bot)
                return

            ask_msg = discord.utils.get(bot.cached_messages, id=ask_msg.id)
            yachu.lockAll()
            for reaction in ask_msg.reactions: #type:discord.Reaction
                if (reaction.emoji not in dice_index_list) or (reaction.emoji == '🆗'): continue
                async for user in reaction.users():
                    if user != player: continue
                    yachu.unlock(dice_index_list.index(reaction.emoji)+1)
                    break

            await ask_msg.delete()
            await phase_msg.delete()
            if yachu.isAllLocked():
                break
            await roll_msg.delete()

        #점수 저장하는 부분
        ask_msg = await chan.send('저장할 항목을 고르고 :ok:버튼을 눌러주세요')
        for button in save_index_list:
            await ask_msg.add_reaction(button)
        try:
            reaction_type, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
        except TimeoutError:
            await chan.send('Timeout!')
            await ng_addpoint(chan, player, -1 * betpoint)
            makefree(bot)
            return
        ind = -1
        breaker = False
        ask_msg = discord.utils.get(bot.cached_messages, id=ask_msg.id)

        for reaction in ask_msg.reactions:  # type:discord.Reaction
            if (reaction.emoji not in save_index_list) or (reaction.emoji == '🆗') : continue
            if breaker: break
            async for user in reaction.users():
                if user != player: continue
                ind = save_index_list.index(reaction.emoji)
                breaker = True
                break
        if ind == -1:
            await chan.send('잘못된 응답입니다. 야추 게임을 종료합니다.')
            await ng_addpoint(chan, player, -1 * betpoint)
            makefree(bot)
            return
        await ask_msg.delete()
        await roll_msg.delete()
        await board_msg.delete()

        yachu.setScore(ind)
        i -= 1


    await chan.send(embed=yachu.getScoreBoard())
    await chan.send(f'{yachu.score[14]}점을 얻으셨습니다!')
    if betpoint > 0:
        if yachu.score[14] < 200:
            await ng_addpoint(chan, player, -1 * betpoint)
            await chan.send('안타깝게도 200점을 획득하지는 못하셨네요. 다음 기회에!')
        else:
            await ng_addpoint(chan, player, betpoint)
            await chan.send(f'200점 이상을 획득하셨네요. {betpoint}점을 획득하였습니다!')
    return


"""async def vs_playing(ctx, user, betpoint):
    yachus = [Yachu(), Yachu()]
    multiyachu = MultiYachu(yachus[0], yachus[1], ctx.author.display_name, user.display_name)
    for i in range(12):
        for j in range(2):
            if j == 0:
                await ctx.send(f'{ctx.author.display_name}님의 차례입니다')
            else:
                await ctx.send(f'{user.display_name}님의 차례입니다')
            await ctx.send(multiyachu.getScoreBoard())
            while yachus[j].phase < 3:
                await ctx.send(yachus[j].rollDice())
                if yachus[j].phase == 3:

                    def func1(msg):
                        this = int(msg.content)
                        if yachus[j].isAvailable(this):
                            return this
                        else:
                            raise ReAsk

                    if j == 0:
                        ind = await question(ctx, '저장할 칸 선택', func1, ctx.author, betpoint)
                    else:
                        ind = await question(ctx, '저장할 칸 선택', func1, user, betpoint)



                else:
                    def func2(msg):
                        this = int(msg.content)
                        if this == 0: return this
                        if yachus[j].isAvailable(this):
                            return this
                        else:
                            raise ReAsk

                    if j == 0:
                        ind = await question(ctx, '저장할 칸 선택, 다시 굴리려면 0', func2, ctx.author, betpoint)
                    else:
                        ind = await question(ctx, '저장할 칸 선택, 다시 굴리려면 0', func2, user, betpoint)

                if ind == -1: return
                if ind == 0:
                    yachus[j].unlockAll()

                    def func3(msg):
                        temp = msg.content.split()
                        if len(temp) == 1 and temp[0] == '0': return
                        for ind in temp:
                            ind = int(ind)
                            yachus[j].lock(ind)
                        return

                    if j == 0:
                        if await question(ctx, '고정할 주사위 선택 - ex) 1 2 4, 없으면 0', func3, ctx.author,
                                          betpoint) == -1: return
                    if j == 1:
                        if await question(ctx, '고정할 주사위 선택 - ex) 1 2 4, 없으면 0', func3, user, betpoint) == -1: return

                else:
                    yachus[j].setScore(ind)
                    break
    await ctx.send(multiyachu.getScoreBoard())
    a, b = multiyachu.getFinalScore()
    await ctx.send(f'{ctx.author.display_name}님이 {a}점, {user.display_name}님이 {b}점 획득하셨네요!')
    if a > b:
        ng_movepoint(ctx, sender=user, receiver=ctx.author, point=betpoint)
    elif a < b:
        ng_movepoint(ctx, sender=ctx.author, receiver=user, point=betpoint)
    else:
        await ctx.send('어케비겼누ㄷ.ㄷ')
    await ctx.send(f'게임 결과에 따라, 각각 {ng_getpoint(ctx.author)}점, {ng_getpoint(user)}점이 되셨습니다!')

    return
"""