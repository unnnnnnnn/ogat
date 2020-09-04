import discord
import asyncio
import os
import random
import json
from discord.utils import get
from discord.ext import commands

# Jeu de 40 cartes: 10x 0, 10x 1, 10x 2, 10x 3
# Il faut 4 joueurs pour jouer
# Chaque joueur a 4 cartes
# On joue chaqun son tour en posant une carte
# On additionne le total à chaque fois
# Quand quelqu'un dépasse 9, cette personne perd

PATH = os.getcwd()

DECK = ['0️⃣','0️⃣','0️⃣','0️⃣','0️⃣','0️⃣','0️⃣','0️⃣','0️⃣','0️⃣','1️⃣','1️⃣','1️⃣','1️⃣','1️⃣','1️⃣','1️⃣','1️⃣','1️⃣','1️⃣','2️⃣','2️⃣','2️⃣','2️⃣','2️⃣','2️⃣','2️⃣','2️⃣','2️⃣','2️⃣','3️⃣','3️⃣','3️⃣','3️⃣','3️⃣','3️⃣','3️⃣','3️⃣','3️⃣','3️⃣']

def setup(client):
    client.add_cog(NymTypeZero(client))

class NymTypeZero(commands.Cog):

    def __init__(self, client):
        self.client = client

    def is_bot():
        def check_bot(ctx):
            return ctx.author.bot
        return commands.check(check_bot)

    @commands.command()
    async def ntzcreate(self, ctx):
        
        cid = str(ctx.channel.id)
        gid = str(ctx.guild.id)

        with open("{}/data/ntz/games.json".format(PATH), encoding='utf-8') as gf:
            gdata = json.load(gf)

        if cid in gdata:
            await ctx.channel.send("❌ A game is already on going in this channel.") 

        else:
            gdata.update({cid:{"players":{}, "bets":0, "started":False, "total":0}})

            with open("{}/data/ntz/games.json".format(PATH), 'w', encoding='utf-8') as gf:
                json.dump(gdata, gf, indent=4, ensure_ascii=False)

            await ctx.channel.send("➡️ A game of **Nym Type Zero** has been created in <#{}>. There is currently 0 player registered. Type ``g.join <bet>`` in this channel to join this game. \n The base amount you need to bet is **5 coins**.".format(ctx.channel.id))

            await asyncio.sleep(60)

            with open("{}/data/ntz/games.json".format(PATH), encoding='utf-8') as gf:
                gdata = json.load(gf)

            if cid in gdata:
                if not gdata[cid]["started"]:

                    with open("{}/users/bank.json".format(PATH), encoding='utf-8') as f:
                        data = json.load(f)

                    for pid in gdata[cid]["players"]:
                        bet = gdata[cid]["players"][pid]["bet"]
                        data[gid]["users"][pid] += int(bet)

                    del gdata[cid]

                    with open("{}/users/bank.json".format(PATH), 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=4, ensure_ascii=False)

                    with open("{}/data/shared/games.json".format(PATH), 'w', encoding='utf-8') as gf:
                        json.dump(gdata, gf, indent=4, ensure_ascii=False)

                    await ctx.channel.send("❌ Game cancelled. The game took too much time to start. Everyone's bets have been returned.")


    @commands.command()
    async def ntzjoin(self, ctx, amount):

        amount = int(amount)
        mid = str(ctx.author.id)
        gid = str(ctx.guild.id)
        cid = str(ctx.channel.id)

        if amount < 5:
            await ctx.channel.send("❌ The required amount to join a game is 5 coins")
        
        else:
            with open("{}/data/ntz/games.json".format(PATH), encoding='utf-8') as gf:
                gdata = json.load(gf)

            if cid in gdata:

                with open("{}/users/bank.json".format(PATH), encoding='utf-8') as f:
                    data = json.load(f)

                    if mid in data[gid]["users"]:

                        if amount > data[gid]["users"][mid]:
                            await ctx.channel.send("❌ You are trying to bet a higher amount than the money you have. Your balance is **{} coins.**".format(data[gid]["users"][mid]))
                        else:
                            gdata[cid]["players"][mid] = {"deck":[]}
                            gdata[cid]["bets"] += amount
                            data[gid]["users"][mid] -= amount

                            with open("{}/users/bank.json".format(PATH), 'w', encoding='utf-8') as f:
                                json.dump(data, f, indent=4, ensure_ascii=False)

                            with open("{}/data/ntz/games.json".format(PATH), 'w', encoding='utf-8') as gf:
                                json.dump(gdata, gf, indent=4, ensure_ascii=False)

                            await ctx.channel.send("✅ <@{}> has registered to a game of **Nym Type Zero** in <#{}>. The total bets amount is **{} coins**. \n There are **{}/4 players** in this game.".format(ctx.author.id, ctx.channel.id, gdata[cid]["bets"], len(gdata[cid]["players"])))

                            if len(gdata[cid]["players"]) == 4:

                                await ctx.channel.send("There are enough players in this game, it will start very soon.")

                                with open("{}/data/ntz/games.json".format(PATH), encoding='utf-8') as gf:
                                    gdata = json.load(gf)

                                gdata[cid]["started"] = True

                                with open("{}/data/ntz/games.json".format(PATH), 'w', encoding='utf-8') as gf:
                                    json.dump(gdata, gf, indent=4, ensure_ascii=False)

                                await ctx.invoke(self.client.get_command('ntzstart'))
    

    @commands.command()
    @is_bot()
    async def show_deck(self, ctx, aid):

        cid = str(ctx.channel.id)
        user = self.client.get_user(aid)

        with open("{}/data/ntz/games.json".format(PATH), encoding='utf-8') as gf:
            gdata = json.load(gf)

        embed = discord.Embed(
            colour = discord.Color.default()
        ).set_author(
            name = "OGAT",
            icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(self.client.user)
        ).add_field(
            name = "🗒️ Your cards are",
            value = ', '.join(gdata[cid]["players"][str(aid)]["deck"]),
            inline = False
        )

        await user.send(embed=embed)


    @commands.command()
    @is_bot()
    async def ntzstart(self, ctx):

        cid = str(ctx.channel.id)

        with open("{}/data/ntz/games.json".format(PATH), encoding='utf-8') as gf:
            gdata = json.load(gf)

        GAME_DECK = [k for k in DECK]

        await ctx.channel.send("🗒️ The cards are being distributed...")

        for i in range(0,10):
            for pid in gdata[cid]["players"]:
                card = random.choice(GAME_DECK)
                gdata[cid]["players"][pid]["deck"].append(card)
                GAME_DECK.remove(card)

        with open("{}/data/ntz/games.json".format(PATH), 'w', encoding='utf-8') as gf:
            json.dump(gdata, gf, indent=4, ensure_ascii=False)

        for pid in gdata[cid]["players"]:
            await ctx.invoke(self.client.get_command('show_deck'), aid=pid)

        await ctx.channel.send("Write either '0', '1', '2' or '3' to choose your card.")
        await ctx.invoke(self.client.get_command('ntzgame'))


    @commands.command()
    @is_bot()
    async def ntzgame(self, ctx):
        
        cid = str(ctx.channel.id)

        with open("{}/data/ntz/games.json".format(PATH), encoding='utf-8') as gf:
            gdata = json.load(gf)

        for pid in gdata[cid]["players"]:
            pid = int(pid)
            player = self.client.get_user(pid)

            with open("{}/data/ntz/games.json".format(PATH), encoding='utf-8') as gf:
                gdata = json.load(gf)
            
            await ctx.channel.send("It's **<@{}>**'s turn \nThe current total amount is: **{}/9**".format(pid, gdata[cid]["total"]))
            await ctx.invoke(self.client.get_command('make_choice'), aid=pid)

            if gdata[cid]["total"] >= 9:
                await ctx.invoke(self.client.get_command('end_round'), aid=pid)
                break
        
    
    @commands.command()
    @is_bot()
    async def make_choice(self, ctx, aid):

        cid = str(ctx.channel.id)

        with open("{}/data/ntz/games.json".format(PATH), encoding='utf-8') as gf:
            gdata = json.load(gf)

        user = self.client.get_user(aid)

        CHOICES = ["0","1","2","3"]
        d = {"0":'0️⃣', "1":'1️⃣', "2":'2️⃣', "3":'3️⃣'}
        d2 = {'0️⃣':"0", '1️⃣':"1", '2️⃣':"2", '3️⃣':"3"}

        def check(message):
            if not message.author.bot:
                return (user == message.author) and message.content in CHOICES and str(message.channel.id) == cid and d[message.content] in gdata[cid]["players"][str(message.author.id)]["deck"]

        try:
            message = await self.client.wait_for("message", check=check, timeout=60)
            cvalue = int(message.content)
            card = d[message.content]
        except asyncio.TimeoutError:
            card = random.choice(list(d2.keys()))
            cvalue = int(d2[card])
        finally:
            gdata[cid]["players"][str(message.author.id)]["deck"].remove(card)
            gdata[cid]["players"]["total"] += cvalue

            with open("{}/data/ntz/games.json".format(PATH), 'w', encoding='utf-8') as gf:
                json.dump(gdata, gf, indent=4, ensure_ascii=False)

            
    @commands.command()
    @is_bot()
    async def end_round(self, ctx, aid):
        
        cid = str(ctx.channel.id)
        gid = str(ctx.guild.id)

        with open("{}/data/ntz/games.json".format(PATH), encoding='utf-8') as gf:
            gdata = json.load(gf)

        embed = discord.Embed(
            colour = discord.Color.default()
        ).set_author(
            name = "OGAT",
            icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(self.client.user)
        ).add_field(
            name = "📜Round's results:",
            value = "The loser is: **{}**. They lost all of their bet money ({} coins) \n \n{}".format(self.client.get_user(aid), gdata[cid]["players"][str(aid)]["bet"], '\n'.join(["``{}`` won **{}** coins.".format(self.client.get_user(int(pid)), gdata[cid]["players"][pid][bet]*2) for pid in gdata[cid]["players"] if int(pid) != aid])),
            inline = False
        )

        await ctx.channel.send(embed=embed)

        with open("{}/users/bank.json".format(PATH), encoding='utf-8') as f:
            data = json.load(f)

        for pid in gdata[cid]["players"]:
            if int(pid) != aid:
                data[gid]["users"][pid] += 2*gdata[cid]["players"][pid][bet]
            
        with open("{}/users/bank.json".format(PATH), 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        