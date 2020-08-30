import discord
import asyncio
import os
import random
import json
from discord.utils import get
from discord.ext import commands

PATH = os.getcwd()

def setup(client):
    client.add_cog(HelpMenu(client))

class HelpMenu(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):

        embed = discord.Embed(
            colour = discord.Color.default()
        )

        embed.set_author(
            name = "OGAT",
            icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(self.client.user)
        )

        embed.add_field(
            name = "🛠️ Player Commands",
            value = "``o!ogat``: Get a random image from the image bank. \n \n``o!get <number>``: Get a specific image. To get the last one added, add `last`. \n \n``o!request <url>``: Request an image. Your image will be added if it's good. Don't request NSFW or you'll be blocked from requesting.",
            inline = False
        )

        embed.add_field(
            name = "🛠️ Admin Commands",
            value = "``o!set <type>``: Assign a channel. Enter '`images`' to set an images channel, and '`games`' to set a games channel. \n \n``o!remove <type>``: Remove a channel from the list. Arguments are the same as the set command.",
            inline = False
        )

        panel = await ctx.channel.send(embed=embed)