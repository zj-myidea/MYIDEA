# !/usr/bin/python3
# Author : Zhoujing
# Date : 2019/5/19 23:07
# Email : 854021135@qq.com
import re
import random
import time
import requests
import tldextract



ua_list = [
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36 Maxthon/5.0',
    'Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN) AppleWebKit/537.36 (KHTML, like Gecko) Version/5.0.1 Safari/537.36'
    ]



def save_2_db(url, html):
    # 暂时打印 数据库问题看看量再想办法解决
    print(url, len(html))

def crawl():
    URL = 'http://news.baidu.com/'
    response = requests.get(URL, headers={'User-agent': random.choice(ua_list)})
    html = response.text

    regex = re.compile(r'href=[\'"]?(.*?)[\'"]')
    links = re.findall(regex, html)
    print('Link number: {}'.format(len(links)))
    urls = []
    for link in links:
        if  not link.startswith('http'):
            continue
        tld = tldextract.extract(link)
        if tld.domain == 'baidu':
            continue
        urls.append(link)

    for url in urls:
        html = requests.get(url, headers={'User-agent':random.choice(ua_list)}).text
        save_2_db(url, html)
    print('OK')

    # Todo 超时处理？ status.code异常处理  301 302  400系列 500系列？  URL怎么管理？下载好的。正在下载的，下载失败的，不用再试的



if __name__ == '__main__':
    crawl()




