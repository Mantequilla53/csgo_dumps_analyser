import datetime
import json
import os
from time import sleep
import pandas as pd
import requests
import re
from dotenv import load_dotenv

load_dotenv()

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

    steam_cookie = os.getenv('COOKIE') if len(os.getenv('COOKIE')) > 50 else input('Enter your Steam Profile Cookies:')
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
    soupProfile = BeautifulSoup(r.content, 'html.parser')

    steam_badges = soupProfile.find('a', class_="persona_level_btn")['href']

    jsonDump = json.loads('{"cursor":"dumby"}')
    df = pd.DataFrame(columns=["Image", "Item", "Icon URL"])
    startTime = datetime.datetime.now()

    pageCount = 0
    while jsonDump is None or 'cursor' in jsonDump:
        inventory_history_url_build = f"{steam_badges[:-6]}inventoryhistory/?ajax=1&cursor[time]={time}&cursor[time_frac]={time_frac}&cursor[]={s}&sessionid={sessionid[0]}&app[]={appid}"
        try:
            dump = requests.get(inventory_history_url_build, headers=headers)
            jsonDump = json.loads(dump.text)
            soupDump = BeautifulSoup(jsonDump['html'], 'html.parser')
            allItemHtml = soupDump.find_all(class_="tradehistoryrow")

            time = str(jsonDump['cursor']['time'])
            s = str(jsonDump['cursor']['s'])
            for id in jsonDump['descriptions'][appid]:
                item = jsonDump['descriptions'][appid][id]
                classid = int(item['classid'])
                #itemHtml = allItemHtml.find("a", attrs={"data-classid" : classid})
                itemHtml = soupDump.select(f'a[data-classid="{classid}"]')
                name = item["market_name"]
                iconurl = f"https://community.cloudflare.steamstatic.com/economy/image/{item['icon_url']}/330x192"
                df.loc[len(df.index)] = [f'=IMAGE("{iconurl}")', name, iconurl]
            pageCount += 1
            print(f"{df.shape[0].__repr__()} records collected. Rate: {df.shape[0]/(datetime.datetime.now() - startTime).total_seconds():.2f}/s")
            sleep(2)
            df.to_csv("output.csv")
        except(Exception):
            print(f"Skipping after {pageCount} pages. | {Exception.__repr__()}")
            sleep(5)
    endTime = datetime.datetime.now()
    print(f"Dump complete at {endTime} (Elapsed: {endTime-startTime}) {df.shape[0]} transactions dumped over {pageCount} pages.")



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
