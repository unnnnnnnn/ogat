import discord
import asyncio
import os
import random
import json
from discord.utils import get
from discord.ext import commands

PATH = os.getcwd()

def setup(client):
    client.add_cog(AdminsManager(client))

class AdminsManager(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def set(self, ctx, arg):

        if ctx.author.guild_permissions.administrator:

            channel = ctx.channel.id

            with open('{}/data/guilds.json'.format(PATH), encoding='utf-8') as f:
                data = json.load(f)

            if arg == 'images':
                if str(ctx.guild.id) in data:
                    data[str(ctx.guild.id)]["images"].append(channel)
                else:
                    data.update({str(ctx.guild.id):{"images":[channel], "games":[]}})
                
                await ctx.channel.send("✅ OGAT can now send images in <#{}> on this server.".format(channel))

            elif arg == 'games':
                if str(ctx.guild.id) in data:
                    data[str(ctx.guild.id)]["games"].append(channel)
                else:
                    data.update({str(ctx.guild.id):{"images":[], "games":[channel]}})
                await ctx.channel.send("✅ Games can now be played in <#{}> on this server.".format(channel))

            else:
                await ctx.channel.send("❌ Wrong argument")

            with open('{}/data/guilds.json'.format(PATH), 'w', encoding='utf-8') as jf:
                json.dump(data, jf, indent=4, ensure_ascii=False)        

        else:
            await ctx.channel.send("❌ Missing Permission")


    @commands.command()
    async def remove(self, ctx, arg):

        if ctx.author.guild_permissions.administrator:

            channel = ctx.channel.id

            with open('{}/data/guilds.json'.format(PATH), encoding='utf-8') as f:
                data = json.load(f)

            if arg == "images" or arg == "games":
                
                if str(ctx.guild.id) in data:
                    if channel in data[str(ctx.guild.id)][arg]:
                        data[str(ctx.guild.id)][arg].remove(channel)

                        with open('{}/data/guilds.json'.format(PATH), 'w', encoding='utf-8') as jf:
                            json.dump(data, jf, indent=4, ensure_ascii=False) 

                        await ctx.channel.send("✅ <#{}> has been removed from the {} channels list".format(channel, arg))

                    else:
                        await ctx.channel.send("❌ This channel is not in the {} channels list.".format(arg))
                else:
                    await ctx.channel.send("❌ There are no {} channels set up.".format(arg))

            else:
                await ctx.channel.send("❌ Wrong argument")
        else:
            await ctx.channel.send("❌ Missing Permission")

    
    @commands.command()
    async def clist(self, ctx):

        if ctx.author.guild_permissions.administrator:

            with open('{}/data/guilds.json'.format(PATH), encoding='utf-8') as f:
                data = json.load(f)

            if str(ctx.guild.id) in data:

                await ctx.channel.send("**Image channels**: {} \n**Game channels**: {}".format(' '.join(["<#{}>".format(idc) for idc in data[str(ctx.guild.id)]["images"]]), ' '.join(["<#{}>".format(idc) for idc in data[str(ctx.guild.id)]["games"]])))