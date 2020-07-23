import Yachu
import discord
from discord.ext import commands


token = open('data/token.txt','r').readline()
game = discord.Game("!야추")
bot = commands.Bot(command_prefix= '!',activity = game)

score = [0]*15
def yachu_base(score):
    return "----점수표----\nAces  :{}\nDeuces:{}\nThrees:{}\nFours :{}\nFives :{}\nSixes :{}\n-------------\nSubtotal:{}\nbonus:{}" \
           "\n-------------\nChoice:{}\nFour Cards:{}\nFull House:{}\nS.Straight:{}\nL.Straight:{}\nYacht:{}\n-------------\nTotal:{}\n".format(*score)

base = yachu_base(score)


@bot.event
async def on_ready():
    print("start")

@bot.command()
async def 야추(msg):
    await msg.send(base)

bot.run(token)

