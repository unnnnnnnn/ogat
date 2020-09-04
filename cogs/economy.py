import discord
import asyncio
import os
import random
import json
from discord.utils import get
from discord.ext import commands

PATH = os.getcwd()

OWNERS = ["157588494460518400"]

def setup(client):
    client.add_cog(Economy(client))

class Economy(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()   
    async def bal(self, ctx, user : discord.user.User = None):

        gid = str(ctx.guild.id)
        
        if user == None:
            mid = str(ctx.author.id)
        else:
            mid = str(user.id)

        with open("{}/users/bank.json".format(PATH), encoding='utf-8') as f:
            data = json.load(f)

        if mid in data[gid]["users"]:
            await ctx.channel.send("<@{}>'s balance in {} is: **{} coins.**".format(int(ctx.author.id), self.client.get_guild(ctx.guild.id), data[gid]["users"][mid]))


    @commands.command()
    async def add(self, ctx, mid, amount):

        gid = str(ctx.guild.id)
        amount = int(amount)

        if ctx.author.guild_permissions.administrator or str(ctx.author.id) in OWNERS:
            if amount < 0:
                await ctx.channel.send("❌ The amount can't be lower than 0 coins")
            else:
                with open("{}/users/bank.json".format(PATH), encoding='utf-8') as f:
                    data = json.load(f)

                if mid in data[gid]["users"]:
                    data[gid]["users"][mid] += amount

                await ctx.channel.send("✅ <@{}> You have added **{}** coins to **{}**'s balance. Their balance is now **{} coins.**".format(ctx.author.id, amount, self.client.get_user(int(mid)).name, data[gid]["users"][mid]))

                with open("{}/users/bank.json".format(PATH), 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)

    @commands.command()
    async def setbal(self, ctx, mid, bal):
        
        gid = str(ctx.guild.id)
        bal = int(bal)

        if ctx.author.guild_permissions.administrator or str(ctx.author.id) in OWNERS:
            if bal < 0:
                await ctx.channel.send("❌ The amount can't be lower than 0 coins")

            else:
                with open("{}/users/bank.json".format(PATH), encoding='utf-8') as f:
                    data = json.load(f)

                if mid in data[gid]["users"]:
                    data[gid]["users"][mid] = bal

                await ctx.channel.send("✅ <@{}> You have set **{}**'s balance to **{} coins.**".format(ctx.author.id, self.client.get_user(int(mid)).name, bal))

                with open("{}/users/bank.json".format(PATH), 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
