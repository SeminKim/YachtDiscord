import time
import requests
import discord
from config import NG_SERVER_URL

def ng_getpoint(user_id, guild_id):
    url = f'{NG_SERVER_URL}?id={user_id}&guild={guild_id}'
    foo = requests.get(url).text
    return int(foo)

async def ng_addpoint(ctx, user:discord.Member, delta:int):
    if delta == 0: return
    with open('data/log.txt', 'a') as f:
        f.write(f'{delta} point added to {user.display_name}, now {ng_getpoint(user.id, ctx.guild.id)}, executed at {time.ctime()}\n')
    await ctx.send(f"!점수추가 {user.mention} {delta}")
    return


def ng_movepoint(ctx, sender, receiver, point):
    ng_addpoint(ctx, receiver, point)
    ng_addpoint(ctx, sender, -1 * point)