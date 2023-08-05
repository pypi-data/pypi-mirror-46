'''
---stpip---
This file contains the code that go scrap the website

@R. Thomas
@Santiago, Chile
@2019
'''


##standard library
import requests
import ast
from datetime import datetime

#local import
from bs4 import BeautifulSoup

def scrap(package):
    '''
    This function go scrap pepy.tech

    Parameters
    -----------
    package
            str, name of the pypi package

    Returns
    -------
    total
            int, total number of downloads, all time
    month
            int, number of downloads in last month
    day
            int, number of downloads in the last week
    last_date
            str, date of the last day the stat was computed
    last_date_down, 
            int, number of downloads during last_date day
    '''

    url = 'https://api.pepy.tech/api/projects/' + package

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    if soup.contents[0][:15] == "doctype html":
        total = 0
        month = 0
        day = 0
        ndays = 0

        last_day = '0'
        last_date = '0 0 0'
        

    else:
        s = ast.literal_eval(soup.contents[0])
        stripdates = list(s['downloads'].keys())
        ndays = len(s['downloads'].values())
     
        total = s['total_downloads']
        month = sum(s['downloads'].values())
        day = sum(list(s['downloads'].values())[:7]) 

        last_day = s['downloads'][stripdates[0]]
        last_date = stripdates[0]

    return total, month, day, last_day, last_date, ndays



