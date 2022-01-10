from discord.ext import commands
import discord
from requests import get
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import os


match_filter = ['escalation', 'spikerush', 'deathmatch', 'competitive', 'unrated', 'replication', None]

cluster = MongoClient(os.getenv('MONGO_LINK'))

db = cluster['Test']
collection = db['test']


#----------------------------------------------------------------------------------------------------------------------------------------------------------


def sort(e):
    return e['ACS']

#----------------------------------------------------------------------------------------------------------------------------------------------------------


def link_func(user_id : int, username : str, tag : str):

    link = f'https://api.henrikdev.xyz/valorant/v1/account/{username}/{tag}'
    r = get(link)

    data = r.json()
    puuid = data['data']["puuid"]

    post = {
        '_id' : user_id,
        'puuid' : puuid,
        'region' : data['data']['region'],
    }

    try:
        collection.insert_one(post)

    except DuplicateKeyError:
        collection.replace_one({'_id' : user_id}, post)

    return puuid



#----------------------------------------------------------------------------------------------------------------------------------------------------------



def get_match(user_id, filter):
    user_data = collection.find_one({'_id' : user_id})

    region = user_data['region']
    puuid = user_data['puuid']

    link = f'https://api.henrikdev.xyz/valorant/v3/by-puuid/matches/{region}/{puuid}'

    if filter == None:

        r = get(link)
        data = r.json()
        return data

    else:
        headers = {'filter' : filter}
        r = get(link, headers)
        data = r.json()
        return data


class Valorant(commands.Cog):
    
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def link(self, ctx, *, playername):

        split = playername.split('#')

        username = split[0]
        tag = split[1]

        puuid = link_func(ctx.author.id, username, tag)
        await ctx.send(f'``{username}#{tag}`` has been linked to this account with the puuid as ``{puuid}``')



#----------------------------------------------------------------------------------------------------------------------------------------------------------


    @commands.command()
    async def recent(self, ctx, filter = None): 

        guild = self.client.get_guild(506485291914100737)

        #All Emojis

        astra = discord.utils.get(guild.emojis, name = 'astra')
        breach = discord.utils.get(guild.emojis, name = 'breach')
        brimstone = discord.utils.get(guild.emojis, name = 'brimstone')
        chamber = discord.utils.get(guild.emojis, name = 'chamber')
        cypher = discord.utils.get(guild.emojis, name = 'cypher')
        jett = discord.utils.get(guild.emojis, name = 'jett')
        kayo = discord.utils.get(guild.emojis, name = 'kayo')
        killjoy = discord.utils.get(guild.emojis, name = 'killjoy')
        omen = discord.utils.get(guild.emojis, name = 'omen')
        phoenix = discord.utils.get(guild.emojis, name = 'phoenix')
        raze = discord.utils.get(guild.emojis, name = 'raze')
        reyna = discord.utils.get(guild.emojis, name = 'reyna')
        sage = discord.utils.get(guild.emojis, name = 'sage')
        skye = discord.utils.get(guild.emojis, name = 'skye')
        sova = discord.utils.get(guild.emojis, name = 'sova')
        viper = discord.utils.get(guild.emojis, name = 'viper')
        yoru = discord.utils.get(guild.emojis, name = 'yoru')
        #neon = discord.utils.get(guild.emojis, name = 'neon)


        #Emoji mapping 

        emojis = {

            'astra' : astra,
            'breach' : breach,
            'brimstone' : brimstone,
            'chamber' : chamber,
            'cypher' : cypher,
            'jett' : jett,
            'kay/o' : kayo,
            'killjoy' : killjoy,
            'omen' : omen,
            'phoenix' : phoenix,
            'raze' : raze,
            'reyna' : reyna,
            'sage' : sage,
            'skye' : skye,
            'sova' : sova,
            'viper' : viper,
            'yoru' : yoru,
            #'neon' : neon,
        }

        #Maps to image mapping

        maps = {
            'ascent' : 'https://trackercdn.com/cdn/tracker.gg/valorant/db/maps/ascent.jpg',
            'bind' : 'https://trackercdn.com/cdn/tracker.gg/valorant/db/maps/bind.jpg',
            'breeze' : 'https://titles.trackercdn.com/valorant-api/maps/2fb9a4fd-47b8-4e7d-a969-74b4046ebd53/splash.png',
            'fracture' : 'https://titles.trackercdn.com/valorant-api/maps/b529448b-4d60-346e-e89e-00a4c527a405/splash.png',
            'haven' : 'https://trackercdn.com/cdn/tracker.gg/valorant/db/maps/haven.jpg',
            'icebox' : 'https://trackercdn.com/cdn/tracker.gg/valorant/db/maps/icebox.jpg',
            'split' : 'https://trackercdn.com/cdn/tracker.gg/valorant/db/maps/split.jpg',
        }
        
        if filter in match_filter:

            data = get_match(ctx.author.id, filter)
            
            map_name = str(data['data'][0]['metadata']['map']).lower()
            mode = str(data['data'][0]['metadata']['mode'])
            rounds_played = int(data['data'][0]['metadata']['rounds_played'])
            match_id = str(data['data'][0]['metadata']['matchid'])

            round_data = data['data'][0]['teams']

            if round_data['red']['has_won'] == True:

                has_won = "Red"
                round_score = f"{round_data['red']['rounds_won']}(Red) : {round_data['blue']['rounds_won']}(Blue)"

            elif round_data['red']['has_won'] and round_data['blue']['has_won'] == False:
                has_won = 'Draw'
                round_score = f"{round_data['red']['rounds_won']}(Red) : {round_data['blue']['rounds_won']}(Blue)"

            else:
                has_won = 'Blue'
                round_score = f"{round_data['blue']['rounds_won']}(Blue) : {round_data['red']['rounds_won']}(Red)"
            


            embed = discord.Embed(title = f"{mode} in {map_name} \n{round_score}")
            embed.set_author(name = mode, icon_url= 'https://cdn.discordapp.com/attachments/894851964406468669/895909536731369472/lmfao.png')
            embed.add_field(name = 'Match ID:', value = f"``{match_id}``", inline = False)
            embed.add_field(name = 'Rounds Played:', value = str(rounds_played), inline = False)
            embed.add_field(name = 'Winning team:', value = has_won, inline = False)
            embed.add_field(name = 'Score:', value = f"``{round_score}``", inline = False)
            embed.set_footer(text ="Requested by " + str(ctx.author))
        
        
            blue_team = []
            red_team = []



            for player in data['data'][0]['players']['blue']:

                
                    kills = str(player['stats']['kills'])
                    deaths = str(player['stats']['deaths']) 
                    assists = str(player['stats']['assists']) 
                    score = int(player['stats']['score']) 
                    character = str(player['character']).lower()

                    ACS = round(score / rounds_played)

                    blue_team.append({'name' : f"{player['name']}#{player['tag']}", 'ACS' : ACS, "kills" : kills, 'deaths' : deaths, 'assists' : assists, 'agent' : character})

            blue_team.sort(key = sort, reverse = True)


            for player in data['data'][0]['players']['red']:

                
                    kills = str(player['stats']['kills'])
                    deaths = str(player['stats']['deaths']) 
                    assists = str(player['stats']['assists']) 
                    score = int(player['stats']['score']) 
                    character = str(player['character']).lower()
                

                    ACS = round(score / rounds_played)

                    red_team.append({'name' : f"{player['name']}#{player['tag']}", 'ACS' : ACS, "kills" : kills, 'deaths' : deaths, 'assists' : assists, 'agent' : character})

            red_team.sort(key = sort, reverse = True)


            blue_1 = blue_team[0]
            blue_1_stats = f"``{blue_1['kills']}/{blue_1['deaths']}/{blue_1['assists']} \nACS = {blue_1['ACS']}``"
            blue_1_emoji = emojis[blue_1['agent']]

            blue_2 = blue_team[1]
            blue_2_stats = f"``{blue_2['kills']}/{blue_2['deaths']}/{blue_2['assists']} \nACS = {blue_2['ACS']}``"
            blue_2_emoji = emojis[blue_2['agent']]

            blue_3 = blue_team[2]
            blue_3_stats = f"``{blue_3['kills']}/{blue_3['deaths']}/{blue_3['assists']} \nACS = {blue_3['ACS']}``"
            blue_3_emoji = emojis[blue_3['agent']]

            blue_4 = blue_team[3]
            blue_4_stats = f"``{blue_4['kills']}/{blue_4['deaths']}/{blue_4['assists']} \nACS = {blue_4['ACS']}``"
            blue_4_emoji = emojis[blue_4['agent']]

            blue_5 = blue_team[4]
            blue_5_stats = f"``{blue_5['kills']}/{blue_5['deaths']}/{blue_5['assists']} \nACS = {blue_5['ACS']}``"
            blue_5_emoji = emojis[blue_5['agent']]



            red_1 = red_team[0]
            red_1_stats = f"``{red_1['kills']}/{red_1['deaths']}/{red_1['assists']} \nACS = {red_1['ACS']}``"
            red_1_emoji = emojis[red_1['agent']]

            red_2 = red_team[1]
            red_2_stats = f"``{red_2['kills']}/{red_2['deaths']}/{red_2['assists']} \nACS = {red_2['ACS']}``"
            red_2_emoji = emojis[red_2['agent']]

            red_3 = red_team[2]
            red_3_stats = f"``{red_3['kills']}/{red_3['deaths']}/{red_3['assists']} \nACS = {red_3['ACS']}``"
            red_3_emoji = emojis[red_3['agent']]

            red_4 = red_team[3]
            red_4_stats = f"``{red_4['kills']}/{red_4['deaths']}/{red_4['assists']} \nACS = {red_4['ACS']}``"
            red_4_emoji = emojis[red_4['agent']]

            red_5 = red_team[4]
            red_5_stats = f"``{red_5['kills']}/{red_5['deaths']}/{red_5['assists']} \nACS = {red_5['ACS']}``"
            red_5_emoji = emojis[red_5['agent']]

            

            

            embed.add_field(name = 'Blue Team:', value = f"{blue_1_emoji} **{blue_1['name']}** \n {blue_1_stats} \n\n {blue_2_emoji} **{blue_2['name']}** \n {blue_2_stats} \n\n {blue_3_emoji} **{blue_3['name']}** \n {blue_3_stats} \n\n {blue_4_emoji} **{blue_4['name']}** \n {blue_4_stats} \n\n {blue_5_emoji} **{blue_5['name']}** \n {blue_5_stats}" , inline = True)

            embed.add_field(name = 'Red Team:', value = f"{red_1_emoji} **{red_1['name']}** \n {red_1_stats} \n\n {red_2_emoji} **{red_2['name']}** \n {red_2_stats} \n\n {red_3_emoji} **{red_3['name']}** \n {red_3_stats} \n\n {red_4_emoji} **{red_4['name']}** \n {red_4_stats} \n\n {red_5_emoji} **{red_5['name']}** \n {red_5_stats}" , inline = True)

            embed.set_image(url = maps[map_name])
            
            await ctx.send(embed = embed)
    


def setup(client):
    client.add_cog(Valorant(client))