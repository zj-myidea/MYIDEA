import logging
import time
from queue import Queue, Empty
from threading import Event
from concurrent.futures import ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://news.cnblogs.com'
NEWS_URL = '/n/page/'
event = Event()
FILE_PATH = 'D:/crawlertest/try1.txt'

executor = ThreadPoolExecutor(max_workers=9)

urls = Queue()
htmls = Queue()
output = Queue()

ua_list = [
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36 Maxthon/5.0',
    'Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN) AppleWebKit/537.36 (KHTML, like Gecko) Version/5.0.1 Safari/537.36'
    ]

def creat_url(start, stop, step=1):
    for i in range(start, stop, step):
        urls.put('{}{}{}'.format(BASE_URL, NEWS_URL, i))

def crwaler():
    while not event.is_set():
        try:
            url = urls.get(True, 1)
            print(url)
            response = requests.get(url)
            htmls.put(response.text)
        except Exception as e:
            if isinstance(e, Empty):
                pass
            else:
                logging.error(e)

def paser():
    while not event.is_set():
        try:
            html = htmls.get(True, 1)
            soup = BeautifulSoup(html, 'lxml')
            targets = soup.find_all('h2', attrs={'class': 'news_entry'})

            for target in targets:
                title, url = target.a.string, target.a.attrs.get('href')
                output.put((title, url))
        except Exception as e:
            if isinstance(e, Empty):
                pass
            else:
                logging.error(e)


def save(filepath):
    while not event.is_set():
        try:
            title, url = output.get(True, 1)
            url = (BASE_URL + url).strip()
            title.strip()
            with open(filepath, 'a', encoding='utf8') as f:
                f.write('title:{} url:{} \n'.format(title, url))
                f.flush()
        except Exception as e:
            if isinstance(e, Empty):
                pass
            else:
                logging.error(e)

executor.submit(creat_url, 1, 10)
executor.submit(paser)
executor.submit(save, FILE_PATH)
for i in range(6):
    executor.submit(crwaler)

while True:
    cmd = input('>>>')
    if cmd == 'q':
        event.set()
        executor.shutdown()
        print('bye')
        time.sleep(2)
        break








