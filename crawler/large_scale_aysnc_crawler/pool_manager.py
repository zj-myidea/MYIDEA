# !/usr/bin/python3
# Author : Zhoujing
# Date : 2019/5/20 17:28
# Email : 854021135@qq.com

import leveldb
import pickle
import time
import urllib.parse as urlparse

class UrlDB:
    status_failure = b'0'
    status_success = b'1'

    def __init__(self, db_name):
        self.name = db_name + '.urldb'
        self.db = leveldb.LevelDB(self.name)

    def load_from_db(self,status):
        urls = []
        for url, _status in self.db.RangeIter():
            if status == _status:
                urls.append(url)

        return urls

    def set_success(self, url):
        if isinstance(url, str):
            url = url.encode('utf8')
        try:
            self.db.Put(url, self.status_success)
            ret = True
        except Exception as e:
            ret = False
        return ret

    def set_failure(self, url):
        if isinstance(url, str):
            url = url.encode('utf8')
        try:
            self.db.Put(url, self.status_failure)
            ret = True
        except Exception as e:
            ret = False
        return ret

    def has(self, url):
        if isinstance(url, str):
            url = url.encode('utf8')
        try:
            status = self.db.Get(url)
            return status
        except:pass
        return False

class UrlPool:

    def __init__(self, pool_name):
        self.name = pool_name
        self.db = UrlDB(pool_name)
        self.pool = {}  # host : {url} 待下载队列
        self.pending = {}  # url : pending_time 正在下载
        self.failure = {}  # url : times 下载失败的
        self.failure_threshold = 3  # 失败下线
        self.pending_threshold = 60  # 下载时间
        self.in_mem_count = 0  #
        self.max_hosts = ['', 0]  # 哪个host URL最多
        self.hub_pool = {}  # {URl : last_query_time}
        self.hub_refresh_span = 0  # 间隔
        self.load_cache()

    def load_cache(self):
        path = self.name + '.pkl'
        try:
            with open('path', 'rb') as f:
                self.pool = pickle.load(f)
            cc = [len(v) for k, v in self.pool]
            print('saved pool loaded! urls:', sum(cc))
        except:
            pass

    def set_hubs(self, urls, hub_refresh_span):
        self.hub_refresh_span = hub_refresh_span
        self.hub_pool = {}
        for url in urls:
            self.hub_pool[url] = 0

    def set_status(self, url, status_code):
        if url in self.pending:
            self.pending.pop(url)

        if status_code == 20:
            self.db.set_success(url)
            return
        if status_code == 404:
            self.db.set_failure(url)
            return
        if url in self.failure:
            self.failure[url] += 1
            if self.failure[url] > self.failure_threshold:
                self.db.set_failure(url)
                self.failure.pop(url)
            else:
                self.add(url)

        else:
            self.failure[url] = 1

    def push_to_pool(self, url):
        host = urlparse.urlparse(url).netloc
        if not host or '.' not in host:
            print('try to push_to_pool with bad url:' ,url)
            return False
        if host in self.pool:
            if url in self.pool[host]:
                return True
            self.pool[host].add(url)
            if len(self.pool[host]) > self.max_hosts[1]:
                self.max_hosts[0], self.max_hosts[1] = host, len(self.pool[host])
        else:
            self.pool[host] = {url}
        self.in_mem_count += 1
        return True

    def add(self,url, always=False):
        if always:
            return self.push_to_pool(url)
        pended_time = self.pending.get(url, 0)
        if time.time() - pended_time < self.pending_threshold:
            print('being downloading ', url)
            return
        if self.db.has(url):
            return
        if pended_time:
            self.pending.pop(url)
        return self.push_to_pool(url)

    def addmany(self, urls, always=False):
        if isinstance(urls, str):
            print('urls is a string ', urls)
            self.add(urls, always)
        else:
            for url in urls:
                self.add(url, always)

    def pop(self, count, hubpercent=50):
        print('max of host:',self.max_hosts)

        url_attr_url = 0
        url_attr_hub = 1
        hubs = {}
        hub_count = count * hubpercent // 100
        for hub in self.hub_pool:
            span = time.time() - self.hub_pool[hub]
            if span < self.hub_refresh_span:
                continue
            hubs[hub] = 1
            self.hub_pool[hub] = time.time()
            if len(hubs) >= hub_count:
                break

        delta = 3 if self.max_hosts * 10 > self.in_mem_count else 1
        left_count = count - len(hubs)
        urls = {}
        for host in self.pool:
            if not self.pool[host]:
                continue
            if self.max_hosts[0] == host:
                while delta > 0:
                    url = self.pool[host].pop()
                    self.max_hosts[1] -= 1
                    if not self.pool[host]:
                        break
                    delta -= 1
            else:
                url = self.pool[host].pop()
            urls[url] = url_attr_url
            self.pending[url] = time.time()
            if len(urls) > left_count:
                break
        self.in_mem_count -= len(urls)
        print('to pop:{} urls:{} hubs:{} hosts:{}').format(count, len(urls), len(hubs), len(self.pool))
        urls.update(hubs)
        return urls

    def size(self):
        return self.in_mem_count

    def empty(self):
        return self.in_mem_count == 0

    def __del__(self):
        path = self.name + '.pkl'
        try:
            with open(path, 'wb') as f:
                pickle.dump(self.pool, f)
                print('self.pool save!')
        except:
            pass


















