import codecs
import datetime
import json
import re
from time import sleep

import requests
from bs4 import BeautifulSoup, Tag

from models import Transaction, Item


def findHtmlDiv(allitemhtml, classname):
    for div in allitemhtml:
        if re.search(classname, str(div)) is not None:
            return div


class Dumper:
    appid = '730'
    steamprofile_url = 'https://steamcommunity.com/my'

    def __init__(self, cookie):
        self.s = self.time = '0'
        self.headers = {
            'Cookie': cookie,
            'User-Agent': 'Mozilla/5.0 (Windows NT 7; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',
            'Accept-Charset': 'UTF-8',
            'Accept-Language': 'en-US;q=0.7,en;q=0.3'
        }
        self.sessionId = re.search('sessionid=(\w+)', cookie)
        self.dumpedItems = []

    def dump(self):
        try:
            userId = self.getUserId()
        except Exception:
            raise ValueError("Invalid Cookies")
        startTime = datetime.datetime.now()
        lastPage = False
        while True:
            pageDump = requests.get(self.getInventoryLink(userId), headers=self.headers)
            jsonPage = json.loads(pageDump.text)
            soupPage = BeautifulSoup(jsonPage['html'], 'html.parser')
            allItemHtml = soupPage.find_all(class_="tradehistoryrow")
            if 'cursor' in jsonPage:
                self.time = str(jsonPage['cursor']['time'])
                self.s = str(jsonPage['cursor']['s'])
            else:
                lastPage = True
            try:
                for event in allItemHtml:
                    transaction = Transaction()
                    transaction.date = event.find(class_="tradehistory_date").contents[0].strip('\t\r\n')
                    transaction.time = event.find(class_="tradehistory_timestamp").text
                    transaction.action = event.find(class_="tradehistory_event_description").text.strip('\t\r\n')

                    give_take = event.find_all(class_="tradehistory_items")
                    for action in give_take:
                        plusminus = action.find(class_="tradehistory_items_plusminus").text
                        event_items = filter(lambda eventItem: type(eventItem) == Tag, action.find(class_="tradehistory_items_group").contents)
                        for x in event_items:
                            item = Item()
                            jsonId = f"{x.attrs['data-classid']}_{x.attrs['data-instanceid']}"
                            jsonItem = jsonPage['descriptions'][self.appid][jsonId]
                            item.name = jsonItem['market_name']
                            item.iconUrl = jsonItem['icon_url']
                            item.nameColor = jsonItem['name_color']
                            item.type = jsonItem['type']

                            if plusminus == "+":
                                transaction.add_item(item)
                            if plusminus == "-":
                                transaction.sub_item(item)
                    self.dumpedItems.append(transaction)
                print(f"Page complete. {len(self.dumpedItems)} transactions collected.")
                sleep(2)
            except Exception:
                print("Skipping...")
            if lastPage:
                break
        endTime = datetime.datetime.now()
        print(
            f"Dump complete at {endTime} (Elapsed: {endTime - startTime}) {len(self.dumpedItems)} transactions collected")

    def getUserId(self):
        r = requests.get(self.steamprofile_url, headers=self.headers)
        soupProfile = BeautifulSoup(r.content, 'html.parser')

        steam_badges = soupProfile.find('a', class_="persona_level_btn")['href']
        return steam_badges[:-6]

    def getInventoryLink(self, userId):
        return f"{userId}inventoryhistory/?ajax=1&cursor[time]={self.time}&cursor[time_frac]=0&cursor[]={self.s}&sessionid={self.sessionId}&app[]={self.appid}"

    def export(self):
        with open(datetime.datetime.now().strftime("%d-%m-%Y %H%M%S.CSGOANALYZER"), 'wb') as f:
            json.dump(self.dumpedItems, codecs.getwriter('utf-8')(f), ensure_ascii=False, default=vars)
