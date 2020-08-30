import discord
import asyncio
import os
import random
import json
from discord.utils import get
from discord.ext import commands

PATH = os.getcwd()

def setup(client):
    client.add_cog(ImagesManager(client))


class ImagesManager(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ogat(self, ctx):

        with open('{}/data/guilds.json'.format(PATH), encoding='utf-8') as f:
            data = json.load(f)

        if str(ctx.guild.id) in data:

            channel = self.client.get_channel(data[str(ctx.guild.id)])

            if ctx.channel == channel:

                with open("{}/data/images.txt".format(PATH), 'r') as f:
                    L = f.readlines()

                img = random.choice(L)

                embed = discord.Embed(
                    colour = discord.Color.default(),
                    title = "Case n°{}".format(L.index(img))
                )

                embed.set_image(
                    url = img
                )

                await channel.send(embed=embed)
            
            else:
                await ctx.channel.send("❌ You are using the wrong channel. Please use this command in <#{}>".format(channel.id))

        else:
            await ctx.channel.send("❌ This server did not set a channel to send image. An admin must use ``o!channel`` in a channel to allow the bot to send images.")


    @commands.command()
    async def get(self, ctx, pos):

        with open('{}/data/guilds.json'.format(PATH), encoding='utf-8') as f:
            data = json.load(f)

        if str(ctx.guild.id) in data:

            channel = self.client.get_channel(data[str(ctx.guild.id)])

            if ctx.channel == channel:

                f = open("{}/data/images.txt".format(PATH), "r")
                L = f.readlines()

                if pos == "last":
                    url = L[-1]
                    embed = discord.Embed(
                        colour = discord.Color.default(),
                        title = "Case n°{}".format(L.index(url))
                    )
                    embed.set_image(
                        url = url
                    )

                    await ctx.channel.send(embed=embed)
                    
                else:

                    try:
                        url = L[int(pos)]
                    except ValueError:
                        await ctx.channel.send("❌ Argument de position non valide (pas un nombre entier).")
                    except IndexError:
                        await ctx.channel.send("❌ Argument de position non valide (nombre trop grand). Le max est {}.".format(len(L)-1))
                    else:
                        embed = discord.Embed(
                            colour = discord.Color.default(),
                            title = "Case n°{}".format(L.index(url))
                        )
                        embed.set_image(
                            url = url
                        )

                        await ctx.channel.send(embed=embed)

            else:
                await ctx.channel.send("❌ You are using the wrong channel. Please use this command in <#{}>".format(channel.id))

        else:
            await ctx.channel.send("❌ This server did not set a channel to send image. An admin must use ``o!channel`` in a channel to allow the bot to send images.")

    
    @commands.command()
    async def request(self, ctx, url):

        with open('{}/data/guilds.json'.format(PATH), encoding='utf-8') as f:
            data = json.load(f)

        if str(ctx.guild.id) in data:

            channel = self.client.get_channel(data[str(ctx.guild.id)])

            if ctx.channel == channel:

                f = open('{}/users/blocklist.txt'.format(PATH), 'r')
                L = f.readlines()
                if str(ctx.author.id) in L or "{}\n".format(str(ctx.author.id)) in L:
                    await ctx.channel.send("<@{}> You are blocked from requesting images to the bot.".format(ctx.author.id))

                else:
                    try:
                        f = open("{}/data/images.txt".format(PATH), "r")
                        L = f.readlines()
                        f.close()

                        embed = discord.Embed(
                            colour = discord.Color.default(),
                            title = "Case n°{}".format(len(L))
                        )
                        embed.set_image(
                            url = url
                        )

                        e = await ctx.channel.send(embed=embed)
                        await e.delete()

                    except discord.errors.HTTPException:
                        await ctx.channel.send('❌ URL is invalid')
                    
                    else:
                        f = open("{}/data/images.txt".format(PATH), "r")
                        L = f.readlines()
                        if url in L:
                            await ctx.channel.send('❌ URL is already in the database')
                        else:
                            a = open("{}/users/admins.txt".format(PATH), 'r')
                            L = a.readlines()
                            if "{}\n".format(str(ctx.author.id)) in L or str(ctx.author.id) in L or ctx.guild.id == 743534084940234772:
                                f = open("{}/data/images.txt".format(PATH), 'a+')
                                f.write("\n{}".format(url))
                                f.close()

                                await ctx.channel.send("Image ajoutée **N°{}**".format(len(open("data/images.txt", "r").readlines())-1))
                            else:
                                await ctx.channel.send("✅ Image request sent.")

                                channel_send = client.get_channel(743534715964751931)
                                await channel_send.send("Cette image a été request par {} ({}) depuis {}".format(ctx.author, ctx.author.id, ctx.guild))
                                aga = await channel_send.send(url)

            else:
                await ctx.channel.send("❌ You are using the wrong channel. Please use this command in <#{}>".format(channel.id))

        else:
            await ctx.channel.send("❌ This server did not set a channel to send image. An admin must use ``o!channel`` in a channel to allow the bot to send images.")

    