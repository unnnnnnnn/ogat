import discord
import asyncio
import os
import random
import json
from discord.utils import get
from discord.ext import commands

PATH = os.getcwd()

def setup(client):
    client.add_cog(Devs(client))

class Devs(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def imgadd(self, ctx, idm):

        chan = self.client.get_channel(743534715964751931)

        if ctx.guild.id == 743534084940234772:
            
            try:
                msg_id = int(idm)
            except:
                await ctx.channel.send("❌ Mauvais ID (pas un entier)")

            else:
                try:
                    msg = await chan.fetch_message(msg_id)
                except:
                    await ctx.channel.send("❌ Cet ID n'est pas correct")
                else:
                    url = msg.content
                    f = open("{}/data/images.txt".format(PATH), "a+")
                    f.write("\n{}".format(url))
                    f.close()

                    f = open("{}/data/images.txt".format(PATH), "r")
                    L = f.readlines()
                    
                    await ctx.channel.send("✅ Image ajoutée. Image n°{}".format(len(L)-1))
                    await ctx.channel.send(url)

    @commands.command()
    async def block(self, ctx, idb):

        if ctx.guild.id == 743534084940234772:
        
            f = open('{}/users/blocklist.txt'.format(PATH), 'r')
            L = f.readlines()
            if idb in L:
                await ctx.channel.send("This user is already in the blocked users list.")
            else:
                f = open("{}/users/blocklist.txt".format(PATH), 'a+')
                f.write("\n{}".format(idb))
                f.close()

                await ctx.channel.send("User ID {} has been successfully blocked".format(idb))

    @commands.command()
    async def admin(self, ctx, ida):

        if ctx.guild.id == 743534084940234772:

            f = open('{}/users/admins.txt'.format(PATH), 'r')
            L = f.readlines()
            if ida in L:
                await ctx.channel.send("This user is already in the admins list.")
            else:
                f = open("{}/users/admins.txt".format(PATH), 'a+')
                f.write("\n{}".format(ida))
                f.close()

                await ctx.channel.send("User ID {} has been successfully added as Admin".format(ida))