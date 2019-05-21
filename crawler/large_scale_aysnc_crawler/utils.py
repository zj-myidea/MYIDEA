# !/usr/bin/python3
# Author : Zhoujing
# Date : 2019/5/19 23:07
# Email : 854021135@qq.com
import re
import random
import time
import traceback
from urllib.parse import urlunparse, urlparse
import requests
import tldextract
import cchardet
import logging

def downloader(url, timeout=10, headers=None, debug=False, binary=False):
    ua_list = [
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36 Maxthon/5.0',
        'Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN) AppleWebKit/537.36 (KHTML, like Gecko) Version/5.0.1 Safari/537.36'
        ]
    _headers = {
        'User-agent':random.choice(ua_list)

    }
    redirccted_url = url
    if headers:
        _headers = headers
    try:
        rep = requests.get(url, headers=_headers, timeout=timeout)
        if binary:
            html = rep.content
        else:
            encoding = cchardet.detect(rep.content)['encoding']
            html = rep.content.decode(encoding)
        status = rep.status_code
        redirccted_url = rep.url
    except Exception as e:
        if debug:
            print(traceback.print_exc())
        msg = 'failed download : {}'.format(url)
        print(msg)
        html = b'' if binary else ''
        status = 0
    return status, html, redirccted_url

g_bin_postfix = {
    'exe', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',
    'pdf',
    'jpg', 'png', 'bmp', 'jpeg', 'gif',
    'zip', 'rar', 'tar', 'bz2', '7z', 'gz',
    'flv', 'mp4', 'avi', 'wmv', 'mkv',
    'apk',
}
g_news_postfix = {
    '.html?', '.htm?', '.shtml?',
    '.shtm?',
}


def clea_url(url:str):
    if not url.startswith('http') and not url.startswith('https'):
        return ''
    for np in g_news_postfix:
        p = url.find(np)
        if p > -1:
            p = url.find('?')
            url = url[:p]
            return url
    up = urlparse(url)
    path = up.path
    if not path:
        path = '/'
    postfix = path.split('.')[-1].lower()
    if postfix in g_bin_postfix:
        return ''

    good_queries = []
    for query in up.query.split('&'):
        qv = query.split('=')
        if qv[0].startswith('spm') or qv[0].startswith('utm_'):
            continue
        if len(qv) == 1:
            continue
        good_queries.append(query)
    query = '&'.join(good_queries)
    url = urlunparse((
        up.scheme,
        up.netloc,
        path,
        up.params,
        up.query,
        '',
    ))
    return url

def init_file_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(20)
    fhandler = logging.FileHandler('./{}'.format(name))
    fhandler.setLevel(20)
    fmt = logging.Formatter(fmt = "%(asctime)s %(name)s %(funcName)s %(message)s")
    fhandler.setFormatter(fmt)
    logger.addHandler(fhandler)
    logger.propagate = True
    return logger



if __name__ == '__main__':
    # print(g_bin_postfix)
    # url = 'http://news.baidu.com/'
    # code, html, r_url = downloader(url)
    # print(code, html, r_url)
    print(clea_url('https://www.yuanrenxue.com/crawler/news-crawler-downloader.html'))


