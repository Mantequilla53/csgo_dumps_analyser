import json
import os

import pandas as pd
import requests
import re
import pandas

from bs4 import BeautifulSoup

csgo_stats_mode = {
    1: 'Dump CS:GO Inventory History',
    2: 'Exit'
}


def header():
    print('CSGO Inventory History Advanced Analyzer')


def print_menu():
    for key in csgo_stats_mode.keys():
        print(key, '--', csgo_stats_mode[key])


def collect_steam_parameters():
    appid = '730'

    steam_cookie = input('Enter your Steam Profile Cookies:')
    sessionid = re.findall('sessionid=(\w+)', steam_cookie)

    time_frac = '0'
    s = '0'
    time = '0'


    headers = {
        'Cookie': steam_cookie,
        'User-Agent': 'Mozilla/5.0 (Windows NT 7; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',
        'Accept-Charset': 'UTF-8',
        'Accept-Language': 'en-US;q=0.7,en;q=0.3'
    }
    steamprofile_url = 'https://steamcommunity.com/my'
    r = requests.get(steamprofile_url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    steam_badges = soup.find('a', class_="persona_level_btn")['href']

    jsonDump = json.loads('{"cursor":"dumby"}')
    df = pd.DataFrame(columns=["Item", "Icon URL"])
    while jsonDump is None or 'cursor' in jsonDump:
        inventory_history_url_build = f"{steam_badges[:-6]}inventoryhistory/?ajax=1&cursor[time]={time}&cursor[time_frac]={time_frac}&cursor[]={s}&sessionid={sessionid[0]}&app[]={appid}"
        print(inventory_history_url_build)
        try:
            dump = requests.get(inventory_history_url_build, headers=headers)
            jsonDump = json.loads(dump.text)
            time = str(jsonDump['cursor']['time'])
            s = str(jsonDump['cursor']['s'])
            for id in jsonDump['descriptions'][appid]:
                item = jsonDump['descriptions'][appid][id]
                name = item["market_name"]
                icon = f"https://community.cloudflare.steamstatic.com/economy/image/{item['icon_url']}/330x192"
                df.loc[len(df.index)] = [name, icon]
            df.to_csv("output.csv")
        except(Exception):
            print(f"Skipping: {Exception}")


if __name__ == '__main__':
    header()
    while True:
        print_menu()
        smb_inventory_mode = ''
        try:
            smb_inventory_mode = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')
        if smb_inventory_mode == 1:  # Dumps inventory into files from steam cookies
            collect_steam_parameters()
        elif smb_inventory_mode == 2:
            print('')
            exit()
        else:
            print('Invalid option. Please enter a number between 1 and 2.')
