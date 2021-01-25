import requests as rq
from bs4 import BeautifulSoup as bs
import datetime
from time import sleep

def date():
    while True:
        a = datetime.date.today()
        b = str(a.day)
        if len(b)==1:
            return (f'0{b}')
        else:
            return b
        sleep(720)


r = rq.get('https://bank.gov.ua/WebSelling/Home/News').text
soup = bs(r, 'lxml')

def check():
    while True:
        num = 0
        find_news = soup.find_all('div', id='accordion')
        for i in find_news:
            num+=1
        return num
        sleep(30)


def find_all():
    while True:
        find_news = soup.find('div', id='collapse1').text
        f = str(find_news.strip())
        find_date = soup.find('span', class_='pull-right').text
        date1 = str(find_date[17:18])
        date()
        if date1 == str(date()):
            return 'Вот что мне удалось найти!\n\n'+ f
        else:
            return f'За сегодня новостей нет.\nПоследняя новость была опубликована {find_date[17::]}'
            sleep(30)


def find_last():
    while True:
        find_news = soup.find('div', id='collapse1').text
        f = str(find_news.strip())
        find_date = soup.find('span', class_='pull-right').text
        return f'Вот последняя новость, которая была аж {find_date[17::]}\n\n'+ f
        sleep(30)
