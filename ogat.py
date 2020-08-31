#-*- coding:utf-8 -*-

import discord
import asyncio
import os
import random
import json
import sys
from discord.utils import get
from discord.ext import commands
from datetime import datetime

sys.path.insert(1, "{}/cogs".format(os.path.dirname(__file__)))
import chelp
import images
import admins
import polls
import devs
import shared
import nymtype
import economy

os.chdir(os.path.dirname(__file__))
client = commands.Bot(command_prefix=";;")
client.remove_command("help")

with open('data/token.txt' ,'r') as f:
    token = f.readline()


@client.event
async def on_ready():
    
    await client.wait_until_ready()
    await client.change_presence(activity=discord.Game(name="o!help"))
    print('✅ {0.user} connecté à {1}'.format(client, datetime.now().strftime("%H:%M:%S")))
    online = client.get_channel(743537675469979819)

    with open("users/bank.json", encoding='utf-8') as f:
        data = json.load(f)

    guilds = [str(guild.id) for guild in client.guilds]

    for gid in guilds:
        if gid not in data:
            data.update({gid:{"name": client.get_guild(int(gid)).name,"users":{}}})
            for user in client.get_guild(int(gid)).members:
                uid = str(user.id)
                if uid not in data and not user.bot:
                    data[gid]["users"][uid] = 100.0

    with open("users/bank.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    await online.send('✅ **{0.user}** connecté à ``{1}``'.format(client, datetime.now().strftime("%H:%M:%S")))


@client.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.channel.send("<@{.id}> Missing argument.".format(ctx.author))


@client.command()
async def reload(ctx, name=None):
    if name:
        try:
            client.reload_extension(name)
            await ctx.channel.send("Cog reloaded")
        except:
            client.load_extension(name)
            await ctx.channel.send("Cog loaded")


client.load_extension("economy")
client.load_extension("shared")
client.load_extension("nymtype")
client.load_extension("devs")
client.load_extension("chelp")
client.load_extension("images")
client.load_extension("admins")
client.run(token)