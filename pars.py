import openpyxl as opx
from time import sleep

import requests as rq
from bs4 import BeautifulSoup as bs


class News():

    def __init__(self, check):
        self.check = check
        with open (check, 'r', encoding= 'utf8') as check:
            check_news = check.read()


    def check1(self):
        r = rq.get('https://bank.gov.ua/WebSelling/Home/News').text
        soup = bs(r, 'lxml')
        find_news = soup.find('div', class_='list-group').text
        f = str(find_news.strip())
        return f