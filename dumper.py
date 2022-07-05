import datetime
import json
import re
import requests
from bs4 import BeautifulSoup

from item import Item


class Dumper:
    appid = '730'
    steamprofile_url = 'https://steamcommunity.com/my'

    def __init__(self, cookie):
        self.s = self.time = '0'
        self.header = {
            'Cookie': cookie,
            'User-Agent': 'Mozilla/5.0 (Windows NT 7; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',
            'Accept-Charset': 'UTF-8',
            'Accept-Language': 'en-US;q=0.7,en;q=0.3'
        }
        self.sessionId = re.find('sessionid=(\w+)', cookie)

    def dump(self):
        userId = self.getUserId(self)
        startTime = datetime.datetime.now()
        dumpedItems = []
        while True:
            pageDump = requests.get(self.getInventoryLink(userId), headers=self.headers)
            jsonPage = json.loads(pageDump.text)
            soupPage = BeautifulSoup(jsonPage['html'], 'html.parser')
            allItemHtml = soupPage.find_all(class_="tradehistoryrow")
            if 'cursor' in jsonPage:
                self.cursorTime = str(jsonPage['cursor']['time'])
                self.s = str(jsonPage['cursor']['s'])
            else:
                lastPage = True

            for id in jsonPage['descriptions'][self.appid]:
                item = Item()
                itemJson = jsonPage['descriptions'][self.appid][id]
                item.classId = itemJson['classid']
                item.name = itemJson["market_name"]
                item.type = itemJson["type"]
                item.icon = itemJson['icon_url']
                item.iconLarge = itemJson['icon_url_large']
                item.nameColor = itemJson['name_color']

                itemHtml = self.findHtmlDiv(allItemHtml, item.classId)
                tradeHistory = self.findHtmlDiv(itemHtml, item.classId)

                if tradeHistory:
                    item.added = '+' in tradeHistory.find(class_="tradehistory_items_plusminus").contents[0].strip(
                        '\t\r\n')

                item.date = itemHtml.find(class_="tradehistory_date").contents[0].strip('\t\r\n')
                item.time = itemHtml.find(class_="tradehistory_date").contents[1].text
                item.action = itemHtml.find(class_="tradehistory_event_description").text.strip('\t\r\n')

                dumpedItems.append(item)
                print(
                    f"{len(dumpedItems)} records collected. Rate: {len(dumpedItems) / (datetime.datetime.now() - startTime).total_seconds():.2f}/s")
                print(item.__repr__())
            if lastPage:
                break
        endTime = datetime.datetime.now()
        print(
            f"Dump complete at {endTime} (Elapsed: {endTime - startTime}) {len(dumpedItems)} transactions collected")

    def getUserId(self):
        r = requests.get(self.steamprofile_url, headers=self.headers)
        soupProfile = BeautifulSoup(r.content, 'html.parser')

        steam_badges = soupProfile.find('a', class_="persona_level_btn")['href']
        return steam_badges[:-6]

    def getInventoryLink(self, userId):
        return f"{userId}inventoryhistory/?ajax=1&cursor[time]={self.time}&cursor[time_frac]=0&cursor[]={self.s}&sessionid={self.sessionId}&app[]={self.appid}"

    def findHtmlDiv(self, allitemhtml, classname):
        for div in allitemhtml:
            if re.search(classname, str(div)) is not None:
                return div
