import time
import requests
import discord
from config import NG_SERVER_URL

def ng_getpoint(user):
    foo = requests.get(NG_SERVER_URL+str(user.id)).text
    return int(foo)

async def ng_addpoint(ctx, user:discord.Member, delta:int):
    with open('data/log.txt', 'a') as f:
        f.write(f'{delta} point added to {user.display_name}, now {ng_getpoint(user)}, executed at {time.ctime()}\n')
    await ctx.send(f"!점수추가 {user.mention} {delta}")
    return


def ng_movepoint(ctx, sender, receiver, point):
    ng_addpoint(ctx, receiver, point)
    ng_addpoint(ctx, sender, -1 * point)