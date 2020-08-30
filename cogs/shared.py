import discord
import asyncio
import os
import random
import json
from discord.utils import get
from discord.ext import commands

# Jeu des biens communs

# Mise initiale pour l'inscription, 5 participants max
# 1e tour: 5 participants ont 5 pièces chacun
# Chaque tour, il y a une taxe de 5 pièces.
# On donne au joueur 5 pièce en plus
# Chaque joueur paye entre 0 et 5 pièces pour la taxe.
# Il pose le reste dans une banque personnelle
# Quand tout le monde a misé, le montant total est révélé
# On multiplie ce montant par 2 et on paye chaque joueur équitablement, peu importe s'ils ont payé la taxe à 100%
# Si le montant n'est pas divisible par 5, on arrondit le montant trouvé pour que son double le soit.
# Par exemple, 13 est arrondi à 15, d'où 15x2 = 30 et 30/5 = 6
# Si le montant est 12, il est arrondi à 10 d'où 10x2 = 20 et 20/5 = 4
# Après chaque révélation du montant, un débat a lieu
# Si 3 personnes sont d'accord pour éliminer quelqu'un, elle est exclue (1 SEULE FOIS AU COURS DE LA PARTIE)
# Si une personne n'a pas réussi à réunir 40 pièces en 5 tours, elle pert sa mise d'inscription et n'obtient rien
# Celui avec le plus de pièce à la fin gagne (à condition d'avoir + de 40 pièces)
# Les répartitions des biens sont: 1e 60% (mise totale), 2e: 30%, 3e: 9%, 4e: 1%, 5e: 0%


# NE PAS OUBLIER DE CHANGER LE ASYCIO.SLEEP()

PATH = os.getcwd()

OWNERS = ["157588494460518400"]

def setup(client):
    client.add_cog(Shared(client))

class Shared(commands.Cog):

    def __init__(self, client):
        self.client = client

    def is_bot():
        def check_bot(ctx):
            return ctx.author.bot
        return commands.check(check_bot)

    @commands.command()
    async def create(self, ctx):

        cid = str(ctx.channel.id)
        gid = str(ctx.guild.id)

        with open("{}/data/shared/games.json".format(PATH), encoding='utf-8') as gf:
            gdata = json.load(gf)

        if cid in gdata:
            await ctx.channel.send("❌ A game is already on going in this channel.") 

        else:
            gdata.update({cid:{"players":{}, "bets":0, "started":False, "shared":0, "voted":False}})

            with open("{}/data/shared/games.json".format(PATH), 'w', encoding='utf-8') as gf:
                json.dump(gdata, gf, indent=4, ensure_ascii=False)

            await ctx.channel.send("➡️ A game has been created in <#{}>. There is currently 0 player registered. Type ``g.join <bet>`` in this channel to join this game. \n The base amount you need to bet is **5 coins**.".format(ctx.channel.id))

            await asyncio.sleep(60)

            with open("{}/data/shared/games.json".format(PATH), encoding='utf-8') as gf:
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
    async def join(self, ctx, amount):

        amount = int(amount)
        mid = str(ctx.author.id)
        gid = str(ctx.guild.id)
        cid = str(ctx.channel.id)

        if amount < 5:
            await ctx.channel.send("❌ The required amount to join a game is 5 coins")
        
        else:
            with open("{}/data/shared/games.json".format(PATH), encoding='utf-8') as gf:
                gdata = json.load(gf)

            if cid in gdata:

                with open("{}/users/bank.json".format(PATH), encoding='utf-8') as f:
                    data = json.load(f)

                    if mid in data[gid]["users"]:

                        if amount > data[gid]["users"][mid]:
                            await ctx.channel.send("❌ You are trying to bet a higher amount than the money you have. Your balance is **{} coins.**".format(data[gid]["users"][mid]))
                        else:
                            gdata[cid]["players"][mid] = {"bank": 0, "vote": False, "bet": amount, "eliminated":False}
                            gdata[cid]["bets"] += amount
                            data[gid]["users"][mid] -= amount

                            with open("{}/users/bank.json".format(PATH), 'w', encoding='utf-8') as f:
                                json.dump(data, f, indent=4, ensure_ascii=False)

                            with open("{}/data/shared/games.json".format(PATH), 'w', encoding='utf-8') as gf:
                                json.dump(gdata, gf, indent=4, ensure_ascii=False)

                            await ctx.channel.send("✅ <@{}> has registered to a game in <#{}>. The total bets amount is **{} coins**. \n There are **{}/5 players** in this game.".format(ctx.author.id, ctx.channel.id, gdata[cid]["bets"], len(gdata[cid]["players"])))

                            if len(gdata[cid]["players"]) == 5:

                                await ctx.channel.send("There are enough players in this game, it will start very soon.")

                                with open("{}/data/shared/games.json".format(PATH), encoding='utf-8') as gf:
                                    gdata = json.load(gf)

                                gdata[cid]["started"] = True

                                with open("{}/data/shared/games.json".format(PATH), 'w', encoding='utf-8') as gf:
                                    json.dump(gdata, gf, indent=4, ensure_ascii=False)


                                await ctx.invoke(self.client.get_command('start'))

    @commands.command()
    @is_bot()
    async def start(self, ctx):
        print("start")
        cid = str(ctx.channel.id)
        
        with open("{}/data/shared/games.json".format(PATH), encoding='utf-8') as gf:
            gdata = json.load(gf)

        for pid in gdata[cid]["players"]:
            gdata[cid]["players"][pid]["bank"] += 5

        await ctx.invoke(self.client.get_command('game'))

    
    @commands.command()
    @is_bot()
    async def game(self, ctx):
        print("game")
        cid = str(ctx.channel.id)

        with open("{}/data/shared/games.json".format(PATH), encoding='utf-8') as gf:
            gdata = json.load(gf)

        turn = 0
        while turn < 5:
            turn += 1
            print(turn)
            for pid in gdata[cid]["players"]:
                
                with open("{}/data/shared/games.json".format(PATH), encoding='utf-8') as gf:
                    gdata = json.load(gf)

                if gdata[cid]["players"][pid]["eliminated"] == False:
                    pid = int(pid)
                    player = self.client.get_user(pid)
                    member = ctx.guild.get_member(pid)

                    try:
                        await member.edit(mute=True, deafen=True)
                    except:
                        pass

                    await ctx.channel.send("It's <@{}>'s turn.".format(pid))

                    await ctx.invoke(self.client.get_command('send_recap'), aid=pid)

            await ctx.channel.send("Everyone has made their choice. It's time for the results.")
            await ctx.invoke(self.client.get_command('results'))
            await ctx.channel.send("⚠️ You now have **5 minutes** to debate !")
            await asyncio.sleep(10) # Changer à 60-120
            
            if gdata[cid]["voted"] == False:
                await ctx.channel.send("📢 A vote will start. You'll receive instructions in your DMs.")
                await ctx.invoke(self.client.get_command('vote'))
        
        await ctx.channel.send("⚠️ **The game is over !**")
        await ctx.invoke(self.client.get_command('end_announcement'))

    
    @commands.command()
    @is_bot()
    async def send_recap(self, ctx, aid):
        
        aaid = aid
        cid = str(ctx.channel.id)

        user = self.client.get_user(aid)

        with open("{}/data/shared/games.json".format(PATH), encoding='utf-8') as gf:
            gdata = json.load(gf)

        embed = discord.Embed(
            colour = discord.Color.from_rgb(200,200,200)
        ).set_author(
            name = "OGAT",
            icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(self.client.user)
        ).add_field(
            name = "Summary",
            value = "You have been given **5 tokens**.\n \nYour current balance is **{} token(s)**".format(gdata[cid]["players"][str(aid)]["bank"]),
            inline = False
        )
        await user.send(embed=embed)
        
        await ctx.invoke(self.client.get_command('take_tax'), aid=int(aaid))

    @commands.command()
    @is_bot()
    async def take_tax(self, ctx, aid):

        cid = str(ctx.channel.id)

        player = self.client.get_user(aid)
        member = ctx.guild.get_member(aid)

        ANSWERS = ['0','1','2','3','4','5']
        with open("{}/data/shared/games.json".format(PATH), encoding='utf-8') as gf:
            gdata = json.load(gf)

        await player.send("🐖 You now need to pay your taxes. Write a number **between 0 and 5** to pay. \nIf you write a number lower than 5, the rest will be added to your token account.")

        def check(message):
            return message.author == player and message.channel.type is discord.ChannelType.private and str(message.content) in ANSWERS

        try:
            msg = await self.client.wait_for("message", check=check, timeout=60)
            tax = msg.content
            await player.send("You choose to give **{} tokens** to the shared bank.".format(tax))
        except asyncio.TimeoutError:
            tax = '5'
            await player.send("You did not answer in time. **5 tokens** were automatically given to the shared bank.")
        finally:
            amount = int(tax)
            gdata[cid]["shared"] += amount
            gdata[cid]["players"][str(aid)]["bank"] += (5-amount)

            with open("{}/data/shared/games.json".format(PATH), 'w', encoding='utf-8') as gf:
                json.dump(gdata, gf, indent=4, ensure_ascii=False)

            try:
                await member.edit(mute=False, deafen=False)
            except:
                pass

    @commands.command()
    @is_bot()
    async def results(self, ctx):

        cid = str(ctx.channel.id)
        
        with open("{}/data/shared/games.json".format(PATH), encoding='utf-8') as gf:
            gdata = json.load(gf)

        sbank = int(gdata[cid]["shared"])
        total = 5 * round(sbank/5)
        total = 2*total

        amount = int(total/5)

        for pid in gdata[cid]["players"]:
            gdata[cid]["players"][pid]["bank"] += amount

        gdata[cid]["shared"] = 0

        embed = discord.Embed(
            colour = discord.Color.from_rgb(200,200,200)
        ).set_author(
            name = "OGAT",
            icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(self.client.user)
        ).add_field(
            name = "Summary",
            value = "The number of tokens in the shared bank is: **{} tokens**. \nTherefore, **{} tokens** have been given to everyone.".format(sbank, amount),
            inline = False
        )
        await ctx.channel.send(embed=embed)
        
        with open("{}/data/shared/games.json".format(PATH), 'w', encoding='utf-8') as gf:
            json.dump(gdata, gf, indent=4, ensure_ascii=False)


    @commands.command()
    @is_bot()
    async def vote(self, ctx):

        cid = str(ctx.channel.id)
        
        with open("{}/data/shared/games.json".format(PATH), encoding='utf-8') as gf:
            gdata = json.load(gf)

        REACTIONS = ["🇦", "🇧", "🇨", "🇩", "🇪"]
        PLAYERS = [int(pid) for pid in gdata[cid]["players"]]

        d = {}
        for i in range(0, len(PLAYERS)):
            d[REACTIONS[i]] = PLAYERS[i]
        L = ["{}: ``{}``".format(react, self.client.get_user(d[react]).name) for react in d]
        L.append("❌: I don't want to vote")

        embed = discord.Embed(
            colour = discord.Color.from_rgb(200,200,200)
        ).set_author(
            name = "OGAT",
            icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(self.client.user)
        ).add_field(
            name = "📜 Voting time",
            value = "React to the emojis to vote ! You can only vote once. \nIf no one votes for **15 seconds**, the vote ends. \n \n{}".format('\n'.join(L)),
            inline = False
        )

        panel = await ctx.channel.send(embed=embed)
        for reaction in REACTIONS:
            await panel.add_reaction(reaction)
        await panel.add_reaction("❌")

        def checkV(reaction, user):
            if not user.bot:
                return user.id in PLAYERS and ((str(reaction.emoji) in REACTIONS or str(reaction.emoji) == "❌")) and reaction.message.id == panel.id and gdata[cid]["players"][str(user.id)]["vote"] == False

        votes = []

        while True:

            try:
                reaction, user = await self.client.wait_for("reaction_add", check=checkV, timeout=15.0)
                gdata[cid]["players"][str(user.id)]["vote"] = True

                with open("{}/data/shared/games.json".format(PATH), 'w', encoding='utf-8') as gf:
                    json.dump(gdata, gf, indent=4, ensure_ascii=False)

                if str(reaction.emoji) in REACTIONS:
                    await ctx.channel.send("<@{}> has voted for **{}**.".format(user.id, self.client.get_user(d[str(reaction.emoji)]).name))
                    votes.append(d[str(reaction.emoji)])
                else:
                    await ctx.channel.send("<@{}> has voted for **nobody**.".format(user.id))
                    votes.append("nobody")

            except asyncio.TimeoutError:
                await ctx.channel.send("The vote is over !")
                try:
                    fvote = max(set(votes), key = votes.count)
                except:
                    fvote = None
                if fvote == "nobody" or fvote == None:
                    await ctx.channel.send("📢 No one has been eliminated !")
                else:
                    if votes.count(fvote) >= 3:
                        await ctx.channel.send("📢 <@{}> Has been eliminated by the vote !".format(fvote))
                        gdata[cid]["voted"] = True

                        gdata[cid]["players"][str(fvote)]["eliminated"] = True

                        with open("{}/data/shared/games.json".format(PATH), 'w', encoding='utf-8') as gf:
                            json.dump(gdata, gf, indent=4, ensure_ascii=False)

                        try:
                            await ctx.guild.get_member(fvote).edit(mute=True)
                        except:
                            pass

                    else:
                        await ctx.channel.send("📢 No one has been eliminated !")

                for pid in gdata[cid]["players"]:
                    gdata[cid]["players"][pid]["vote"] = False

                with open("{}/data/shared/games.json".format(PATH), 'w', encoding='utf-8') as gf:
                    json.dump(gdata, gf, indent=4, ensure_ascii=False)
                
                break


    @commands.command()
    @is_bot()
    async def end_announcement(self, ctx):

        cid = str(ctx.channel.id)
        gid = str(ctx.guild.id)

        with open("{}/data/shared/games.json".format(PATH), encoding='utf-8') as gf:
            gdata = json.load(gf)

        with open("{}/users/bank.json".format(PATH), encoding='utf-8') as f:
            data = json.load(f)

        PLAYERS = [int(pid) for pid in gdata[cid]["players"] if gdata[cid]["players"][pid]["eliminated"] == False] 
        if len(gdata[cid]["players"]) == 5:
            EMOJIS = ["🥇", "🥈", "🥉", "4", "5"]
        else:
            EMOJIS = ["🥇", "🥈", "🥉", "4"]

        pdict = {k:v["bank"] for (k,v) in gdata[cid]["players"].items()}
        di = {k: v for k, v in sorted(pdict.items(), key=lambda item: item[1], reverse=True)}

        PLAYERS = [int(pid) for pid in di]
        
        d = {}
        for i in range(0, len(PLAYERS)):
            d[PLAYERS[i]] = EMOJIS[i]

        embed = discord.Embed(
            colour = discord.Color.from_rgb(200,200,200)
        ).set_author(
            name = "OGAT",
            icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(self.client.user)
        ).add_field(
            name = "📜 The game has ended !",
            value = "The game has ended: here are the results \n \n{}".format('\n'.join(["{} ``{}`` with **{} tokens**".format(d[pid], self.client.get_user(pid).name, gdata[cid]["players"][str(pid)]["bank"]) for pid in d])),
            inline = False
        )

        await ctx.channel.send(embed=embed)
        
        AMOUNTS = [0.60 * gdata[cid]["bets"], 0.30 * gdata[cid]["bets"], 0.09 * gdata[cid]["bets"], 0.01 * gdata[cid]["bets"], 0]

        if len(PLAYERS) == 4:
            AMOUNTS.pop(-1)

        for i in range(0,len(PLAYERS)):
            if gdata[cid]["players"][str(PLAYERS[i])]["bank"] >= 40:
                data[gid]["users"][str(PLAYERS[i])] += AMOUNTS[i]
                await ctx.channel.send("<@{}> has therefore received **{} coins** !".format(PLAYERS[i], AMOUNTS[i]))
            else:
                await ctx.channel.send("<@{}> has therefore received **0 coins** because they didn't get 40 tokens !.".format(PLAYERS[i]))

        await ctx.channel.send("❗ **The game is over, thanks for playing !**")
        del gdata[cid]

        with open("{}/data/shared/games.json".format(PATH), 'w', encoding='utf-8') as gf:
            json.dump(gdata, gf, indent=4, ensure_ascii=False)

        with open("{}/users/bank.json".format(PATH), 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        

        
            




        

