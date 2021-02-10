from time import sleep
import requests as rq
from bs4 import BeautifulSoup as bs


class News():
    '''Класс поиска и проверки новостей'''

    def __init__(self, check):
        self.check = check


    '''Считывание файла проверки'''
    def read_check(self):
        with open (self.check, 'r') as file:
            read = file.read()
            return read


    '''Поиск новости для рассылки'''
    def check_news1(self):
        r = rq.get('https://bank.gov.ua/WebSelling/Home/News').text
        soup = bs(r, 'lxml')
        find_news = soup.find('div', class_='list-group').text
        f = str(find_news.strip())
        return f

    '''Ответ на кнопку последней новости'''
    def check_last(self):
        r = rq.get('https://bank.gov.ua/WebSelling/Home/News').text
        soup = bs(r, 'lxml')
        find_news = soup.find('div', class_='list-group').text
        f = str(find_news.strip())
        return f'Вот последняя новость: \n\n{f} '

    '''Проверка кол-ва новостей'''
    def check_point(self):
        r = rq.get('https://bank.gov.ua/WebSelling/Home/News').text
        soup = bs(r, 'lxml')
        check_point = soup.find_all('div', id= 'accordion')
        a = 0
        for item in check_point:
            a+=1
        return str(a)

    '''Перезапись файла проверки'''
    def write_check_point(self):
        with open (self.check, 'w') as file:
            file.write(self.check_point())