import datetime
import json
import os
from time import sleep
import pandas as pd
import requests
import re

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
