from pymongo import MongoClient
import matplotlib.pyplot as plt
from discord.ext import commands
from PIL import Image, ImageDraw
from Modules.PIL_functions import drawProgressBar, moveImage
from Modules.Valorant_stats import get_stats
import discord
import requests
import os


#-------------------------------------------------------------------------------------------------------------------------------------------------------


cluster = MongoClient(os.getenv('MONGO_LINK'))

db = cluster['Test']
collection = db['test']


#-------------------------------------------------------------------------------------------------------------------------------------------------------

async def get_puuid(user_id : int, ctx = None):

    user_data = collection.find_one({'_id' : user_id})
    
    try:

        puuid = user_data['puuid']

        return puuid
        
    except TypeError:
         await ctx.send('Link your discord account with your riot account using the .link command')




#-------------------------------------------------------------------------------------------------------------------------------------------------------


def chkList(lst):
    return len(set(lst)) == 1


#-------------------------------------------------------------------------------------------------------------------------------------------------------





    
def filtering(puuid):

    mmrhist_link = f'https://api.henrikdev.xyz/valorant/v1/by-puuid/mmr-history/ap/{puuid}'

    mmrhist_data = requests.get(mmrhist_link).json()

    elo_list = []

    for mmr in mmrhist_data['data']:
        elo_list.append(mmr['elo'])


    check_list = []

    for elo in elo_list:

        if len(str(elo)) == 2:
            check_list.append(int(elo)) 

        elif len(str(elo)) == 3:
                check_list.append(int(list(str(elo))[0]))

        elif len(str(elo)) == 4:
            check_list.append(int(list(str(elo))[0] + list(str(elo))[1]))


    max_value = str(max(check_list))


    final_list = []

    if chkList(check_list) ==  True:

       top = 100

       for elo in elo_list:


           if len(str(elo)) == 2:

               final_list.append(int(elo))

           elif len(str(elo)) == 3:

                first_digit = list(str(elo))[0] = '0'
                new_number = first_digit + list(str(elo))[1] + list(str(elo))[2]
                final_list.append(int(new_number))

           elif len(str(elo)) == 4:

                first_digit = list(str(elo))[0] = '0'
                second_digit = list(str(elo))[1] = '0'
                new_number = first_digit + second_digit + list(str(elo))[2] + list(str(elo))[3]
                final_list.append(int(new_number))


       return top, final_list

    elif chkList(check_list) == False:

        top = 200

        for elo in elo_list:
      

            if len(str(elo)) == 2:

                final_list.append(int(elo))

            elif len(str(elo)) == 3:

                if list(str(elo))[0] == max_value:

                    first_digit = list(str(elo))[0] = '1'
                    new_number = first_digit + list(str(elo))[1] + list(str(elo))[2]
                    final_list.append(int(new_number))

                elif  list(str(elo))[0] != max_value:

                    first_digit = list(str(elo))[0] = '0'
                    new_number = first_digit + list(str(elo))[1] + list(str(elo))[2]
                    final_list.append(int(new_number))


            elif len(str(elo)) == 4:

                if list(str(elo))[0] + list(str(elo))[1] == max_value:

                    first_digit = list(str(elo))[0] = '0'
                    second_digit = list(str(elo))[1] = '1'
                    new_number = first_digit + second_digit + list(str(elo))[2] + list(str(elo))[3]
                    final_list.append(int(new_number))

                if list(str(elo))[0] + list(str(elo))[1] != max_value:

                    first_digit = list(str(elo))[0] = '0'
                    second_digit = list(str(elo))[1] = '0'
                    new_number = first_digit + second_digit + list(str(elo))[2] + list(str(elo))[3]
                    final_list.append(int(new_number))

        return top, final_list
    


#-------------------------------------------------------------------------------------------------------------------------------------------------------


def mmr(puuid):

    link = f'https://api.henrikdev.xyz/valorant/v2/by-puuid/mmr/ap/{puuid}'

    http_proxy = 'https://203.192.217.11:8080'


    proxies = {
        "http" : http_proxy
    }

    data = requests.get(link, proxies = proxies).json() 

    print(data)

    # name = data['data']['name']
    # tag = data['data']['tag']

    # account_link = f'https://api.henrikdev.xyz/valorant/v1/account/{name}/{str(tag)}'

    
    
    # account_data = requests.get(account_link).json()

    # rank = data['data']['current_data']['currenttierpatched']
    # rank_in_tier = data['data']['current_data']['ranking_in_tier']
    # mmr_change = data['data']['current_data']['mmr_change_to_last_game']
    # account_level = account_data['data']['account_level']
    # player_card = account_data['data']['card']['small']

    # if mmr_change > 0:
    #     mmr_change = '+' + str(mmr_change)




    # return name, tag, rank, rank_in_tier, mmr_change, account_level, player_card

    

#-------------------------------------------------------------------------------------------------------------------------------------------------------


def graph(puuid):

    name, tag, rank, rank_in_tier, mmr_change, account_level, player_card = mmr(puuid)

    top, final_list = filtering(puuid)

    final_list.reverse()

    plt.figure(facecolor = '#2f3136')


    ax = plt.axes()

    title = plt.title(f'MMR Graph for {name}#{tag}')
    ylabel = plt.ylabel('MMR')
    xlabel = plt.xlabel(rank)

    plt.setp(title, color = 'white')
    plt.setp(ylabel, color = 'white')
    plt.setp(xlabel, color = 'white')

    ax.set_facecolor('#2f3136')
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.xaxis.label.set_color('white')


    ax.tick_params(axis = 'x', colors= '#2f3136')
    ax.tick_params(axis = 'y', colors='white')


    for i, v in enumerate(final_list):
        ax.text(i, v+5, '%d' %v, ha = 'center', color = 'white')

    plt.ylim(0, top)



    plt.plot(final_list, label = 'funny', linestyle = 'dotted', color = 'white', linewidth = 2, marker = 'o', markerfacecolor = 'white')

    out = Image.new("RGBA", (460, 50), (0, 0, 0, 0))
    image = ImageDraw.Draw(out)


    #draw the progress bar to given location, width, progress and color
    drawProgressBar(image, 10, 10, 400, 25, rank_in_tier/100, bg = 'white', fg = '#53dbc7')

    out.save('./Images/loading_bar.png')
    plt.savefig('./Images/mmr_graph.png')

    moveImage(f"./Ranks/{str(rank).replace(' ', '_')}.png", "./Images/loading_bar.png")
    

#-------------------------------------------------------------------------------------------------------------------------------------------------------



class Stats(commands.Cog):
    def __init__(self, client):
        self.client = client


#-------------------------------------------------------------------------------------------------------------------------------------------------------


    @commands.command(name = 'comp')
    async def comp(self, ctx):

        guild = self.client.get_guild(506485291914100737)
        loading_emoji = discord.utils.get(guild.emojis, name = 'loading')
        msg = await ctx.send(f"{loading_emoji} Getting Stats")

        puuid = await get_puuid(ctx.author.id)

        graph(puuid)

        name, tag, rank, rank_in_tier, mmr_change, account_level, player_card = mmr(puuid)

        win_percentage, headshot_percentage, kd_ratio, top_weapon, top_agent = get_stats(name, tag, gamemode = 'competitive')


        rank_emoji = discord.utils.get(guild.emojis, name = str(rank).replace(' ', '_'))
        top_agent_emoji = discord.utils.get(guild.emojis, name = top_agent.lower())



        embed = discord.Embed(title = f'Stats for {name}#{tag}', color = discord.Color(0xfa4454))
        embed.set_author(name = 'Competitive Stats', icon_url = ctx.author.avatar_url)
        embed.set_thumbnail(url = player_card)
        embed.add_field(name = 'Account Level:', value = account_level, inline = False)
        embed.add_field(name = "Current rank:", value = f"{rank_emoji} {rank}", inline = True)
        embed.add_field(name = "Current MMR:", value = f"{rank_in_tier}({mmr_change})", inline = True)
        embed.add_field(name = 'K/D ratio:', value = kd_ratio, inline = True)
        embed.add_field(name = 'Win %:', value = win_percentage, inline = True)
        embed.add_field(name = 'Headshot %:', value = headshot_percentage, inline = True)
        embed.add_field(name = 'Most Used Weapon:', value = top_weapon, inline = False)
        embed.add_field(name = 'Most Used Agent:', value = f'{top_agent_emoji} {top_agent}', inline = True)
        


        send = discord.File("./Images/send.png")
        
        embed.set_image(url = 'attachment://send.png')



        mmr_embed = discord.Embed(type = 'image', color = discord.Color(0xfa4454))
        mmr_graph = discord.File("./Images/mmr_graph.png")  
        
        mmr_embed.set_image(url = ('attachment://mmr_graph.png'))

        await msg.delete()
        await ctx.send(file = send, embed = embed)
        await ctx.send(file = mmr_graph, embed = mmr_embed)


#-------------------------------------------------------------------------------------------------------------------------------------------------------

def setup(client):
    client.add_cog(Stats(client))