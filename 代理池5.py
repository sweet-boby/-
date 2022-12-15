
import requests

import random

from lxml import etree

import time

proxy = {
    'http':'49.235.194.72'
}

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.56'
}

x_path = '//tr/td[1]/text()'
# bpool = []

def apool_ap(n,x_path):
    ip_url = 'https://www.toolbaba.cn/ip?p={}'
    resp = requests.get(ip_url.format(n),headers=headers,proxies=proxy)
    resp.encoding='gbk'
    e = etree.HTML(resp.text)
    tree = e.xpath(x_path)
    for x in tree:
        ip = {'http': f'{x}'}
        apool.append(ip)

def bpool_ap(apool):
    for i in apool:
        baidu_url = 'http://www.baidu.com/'
        proxy = i
        try:
            resp = requests.get(baidu_url,headers=headers,proxies=proxy,timeout=0.1)
            if resp.status_code==200:
                bpool.append(i)
                print('ip合格')
        except:
            print('ip不合格')

apool = []
bpool = []

def pool():
    for i in range(1,3):
        apool_ap(i,x_path)
        print(len(apool))
    bpool_ap(apool)
    print(len(bpool))
ks = time.time()
pool()
js = time.time()
print(ks - js )