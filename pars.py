from time import sleep
import requests as rq
from bs4 import BeautifulSoup as bs


class News():

    def __init__(self, check):
        self.check = check
        with open (check, 'r', encoding= 'utf8'):
            pass


    def read_check(self):
        with open (self.check, 'r') as file:
            read = file.read()
            return read



    def check_news1(self):
        r = rq.get('https://bank.gov.ua/WebSelling/Home/News').text
        soup = bs(r, 'lxml')
        find_news = soup.find('div', class_='list-group').text
        f = str(find_news.strip())
        return f

    def check_last(self):
        r = rq.get('https://bank.gov.ua/WebSelling/Home/News').text
        soup = bs(r, 'lxml')
        find_news = soup.find('div', class_='list-group').text
        f = str(find_news.strip())
        return f'Вот последняя новость: \n\n{f} '

    def check_point(self):
        r = rq.get('https://bank.gov.ua/WebSelling/Home/News').text
        soup = bs(r, 'lxml')
        check_point = soup.find_all('div', id= 'accordion')
        a = 0
        for item in check_point:
            a+=1
        return str(a)

    def write_check_point(self):
        with open (self.check, 'w') as file:
            file.write(self.check_point())
