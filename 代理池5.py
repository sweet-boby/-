
import requests

import random

from lxml import etree

import time

from concurrent.futures import ThreadPoolExecutor
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
    print(len(apool))


def bpool_ap(ip):
    # for i in apool:
    baidu_url = 'https://wallhaven.cc/hot'
    proxy = ip
    try:
        resp = requests.get(baidu_url,headers=headers,proxies=proxy,timeout=0.5)
        if resp.status_code==200:
            bpool.append(ip)
            print('ip合格')
    except:
        print('ip不合格')
    print(len(bpool))


apool = []
bpool = []

def pool():
    ks = time.time()
    for i in range(1,100):
        apool_ap(i,x_path)
    with ThreadPoolExecutor(100)as f:
        for ip in apool:
            f.submit(bpool_ap,ip)
    js = time.time()
    print(ks - js )

if __name__ == '__main__':
    pool()
    import json
    with open('ip1.txt','w')as f:
        json.dump(bpool,f)


# import random
# import json
# with open('ip.txt','r')as f:
#     content = f.read()
#     proxies = json.loads(content)
# print(len(proxies))
# proxy = random.choice(proxies)

