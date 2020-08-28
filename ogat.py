#-*- coding:utf-8 -*-

import discord
import asyncio
import os
import random
import json
from discord.utils import get
from discord.ext import commands
from datetime import datetime

os.chdir(os.path.dirname(__file__))
client = commands.Bot(command_prefix="o!")
client.remove_command("help")

with open('token.txt' ,'r') as f:
    token = f.readline()


@client.event
async def on_ready():
    
    await client.wait_until_ready()
    await client.change_presence(activity=discord.Game(name="o!help"))
    print('✅ {0.user} connecté à {1}'.format(client, datetime.now().strftime("%H:%M:%S")))
    online = client.get_channel(743537675469979819)
    await online.send('✅ **{0.user}** connecté à ``{1}``'.format(client, datetime.now().strftime("%H:%M:%S")))

@client.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.channel.send("<@{.id}> Missing argument.".format(ctx.author))
    
    elif isinstance(error, commands.CommandNotFound):
        await ctx.channel.send("<@{.id}> Command does not exist.".format(ctx.author))


@client.command()
async def help(ctx):


    embed = discord.Embed(
        colour = discord.Color.default()
    )

    embed.set_author(
        name = "OGAT",
        icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
    )

    f = open("data.txt", "r")
    L = f.readlines()

    embed.add_field(
        name = "🛠️ Player Commands",
        value = "``o!ogat``: Get a random image from the image bank. \n \n``o!get <number>``: Get a specific image. The max you can select now is {}. \n \n``o!request <url>``: Request an image. Your image will be added if it's good. Don't request NSFW or you'll be blocked from requesting.".format(len(L)-1),
        inline = False
    )

    embed.add_field(
        name = "🛠️ Admin Commands",
        value = "``o!channel``: Set the channel used to send images. Images can't be sent from other channels.",
        inline = False
    )


    panel = await ctx.channel.send(embed=embed)


@client.command()
async def channel(ctx):

    if ctx.author.guild_permissions.administrator:

        channel = ctx.channel.id

        with open('guilds.json', encoding='utf-8') as f:
            data = json.load(f)

        data[str(ctx.guild.id)] = channel

        with open('guilds.json', 'w', encoding='utf-8') as jf:
            json.dump(data, jf, indent=4, ensure_ascii=False)

        await ctx.channel.send("✅ OGAT will now only send images the channel <#{}> on this server.".format(channel))

    else:
        await ctx.channel.send("❌ Missing Permission")


@client.command()
async def ogat(ctx):

    with open('guilds.json', encoding='utf-8') as f:
        data = json.load(f)

    if str(ctx.guild.id) in data:

        channel = client.get_channel(data[str(ctx.guild.id)])

        if ctx.channel == channel:

            with open("data.txt", 'r') as f:
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



@client.command()
async def get(ctx, pos):

    with open('guilds.json', encoding='utf-8') as f:
        data = json.load(f)

    if str(ctx.guild.id) in data:

        channel = client.get_channel(data[str(ctx.guild.id)])

        if ctx.channel == channel:

            f = open("data.txt", "r")
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



@client.command()
async def request(ctx, url):

    with open('guilds.json', encoding='utf-8') as f:
        data = json.load(f)

    if str(ctx.guild.id) in data:

        channel = client.get_channel(data[str(ctx.guild.id)])

        if ctx.channel == channel:

            f = open('blocklist.txt', 'r')
            L = f.readlines()
            if str(ctx.author.id) in L or "{}\n".format(str(ctx.author.id)) in L:
                await ctx.channel.send("<@{}> You are blocked from requesting images to the bot.".format(ctx.author.id))

            else:
                try:
                    f = open("data.txt", "r")
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
                    f = open("data.txt", "r")
                    L = f.readlines()
                    if url in L:
                        await ctx.channel.send('❌ URL is already in the database')
                    else:
                        a = open("admins.txt", 'r')
                        L = a.readlines()
                        if "{}\n".format(str(ctx.author.id)) in L or str(ctx.author.id) in L or ctx.guild.id == 743534084940234772:
                            f = open("data.txt", 'a+')
                            f.write("\n{}".format(url))
                            f.close()

                            await ctx.channel.send("Image ajoutée **N°{}**".format(len(open("data.txt", "r").readlines())-1))
                        else:
                            await ctx.channel.send("✅ Image request sent.")

                            channel_send = client.get_channel(743534715964751931)
                            await channel_send.send("Cette image a été request par {} ({}) depuis {}".format(ctx.author, ctx.author.id, ctx.guild))
                            aga = await channel_send.send(url)

        else:
            await ctx.channel.send("❌ You are using the wrong channel. Please use this command in <#{}>".format(channel.id))

    else:
        await ctx.channel.send("❌ This server did not set a channel to send image. An admin must use ``o!channel`` in a channel to allow the bot to send images.")



@client.command()
@commands.has_any_role("OGAT Master")
async def add(ctx, idm):

    chan = client.get_channel(743534715964751931)

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
                f = open("data.txt", "a+")
                f.write("\n{}".format(url))
                f.close()

                f = open("data.txt", "r")
                L = f.readlines()
                
                await ctx.channel.send("✅ Image ajoutée. Image n°{}".format(len(L)-1))
                await ctx.channel.send(url)




@client.command()
@commands.has_any_role("OGAT Master")
async def block(ctx, idb):

    if ctx.guild.id == 743534084940234772:
    
        f = open('blocklist.txt', 'r')
        L = f.readlines()
        if idb in L:
            await ctx.channel.send("This user is already in the blocked users list.")
        else:
            f = open("blocklist.txt", 'a+')
            f.write("\n{}".format(idb))
            f.close()

            await ctx.channel.send("User ID {} has been successfully blocked".format(idb))



@client.command()
@commands.has_any_role("OGAT Master")
async def admin(ctx, ida):

    if ctx.guild.id == 743534084940234772:

        f = open('admins.txt', 'r')
        L = f.readlines()
        if ida in L:
            await ctx.channel.send("This user is already in the admins list.")
        else:
            f = open("admins.txt", 'a+')
            f.write("\n{}".format(ida))
            f.close()

            await ctx.channel.send("User ID {} has been successfully added as Admin".format(ida))


client.run(token)