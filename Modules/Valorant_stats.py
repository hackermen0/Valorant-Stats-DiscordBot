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


    return win_percentage, headshot_percentage, kd_ratio, top_weapon, top_agent







