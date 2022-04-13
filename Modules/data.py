from requests import get
from bs4 import BeautifulSoup
import re


def get_stats(username, tag, gamemode):

    username = username.replace(' ', '%20')

    link = f'https://tracker.gg/valorant/profile/riot/{username}%23{tag}/overview?playlist={gamemode}'

    data = get(link).text

    soup = BeautifulSoup(data, 'lxml').text

    headshot = re.findall('Headshot%  \d+\.\d+%', soup)

    win = re.findall('Win %  \d+\.\d+%', soup)

    kd = re.findall('K/D Ratio  \d+\.\d+', soup)


    top_weapon = re.findall('Top Weapons   (\w+)', soup)[0]

    top_agent = re.findall('Kills / Match   (\w+)', soup)[0]

    headshot_percentage = headshot[0].split('Headshot%')[1].replace(' ', '')

    win_percentage = win[0].split('Win %')[1].replace(' ', '')

    kd_ratio = kd[0].split('K/D Ratio')[1].replace(' ', '')

    print(data, soup)

    print(win_percentage, headshot_percentage, kd_ratio, top_weapon, top_agent)


    return win_percentage, headshot_percentage, kd_ratio, top_weapon, top_agent


def agent_data(username, tag, gamemode):

    all_agent_data = []

    output_data = []

    some = []

    link = f'https://tracker.gg/valorant/profile/riot/{username}%23{tag}/agents?playlist={gamemode}'

    data = get(link).text

    soup = BeautifulSoup(data, 'lxml').text


    agents = re.findall('(\w+) Played', soup)
    agent_time = re.findall('Played \d+\w+ \d+\w+ \d+\w+ \n              \d+\n            \n              \d+\.\d+%\n            \n              \d+\.\d+\n            \n              \d+ / \d+ / \d+\n            \n              \d+\.\d+\n            \n              \d+\.\d+', soup)
    agent_time2 = re.findall('Played \d+\w+ \d+\w+ \n              \d+\n            \n              \d+\.\d+%\n            \n              \d+\.\d+\n            \n              \d+ / \d+ / \d+\n            \n              \d+\.\d+\n            \n              \d+\.\d+', soup)



    # print(agent_time, agent_time2)
    for item in agent_time:
        new_item = str(item).replace('\n', '&').replace(' ', '').replace('&&', '&')
        all_agent_data.append(new_item)
        
    for item in agent_time2:
        new_item = str(item).replace('\n', '&').replace(' ', '').replace('&&', '&')
        all_agent_data.append(new_item)


    for pos, agent in enumerate(agents):
        if agent == 'O':
            agent = 'KAY/O'
        some.append({agent : all_agent_data[pos]})

    for item in some:
        for agent_name, agent_stats in item.items():
            
            split_stats = agent_stats.split('&')
            output_data.append([agent_name, split_stats])

    return output_data










