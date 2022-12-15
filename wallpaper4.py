
import requests

import random

from lxml import etree

import json
import time
import asyncio
import aiohttp
import aiofiles

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.56'
}
async def requ(url,session,name):
    async with session.get(url) as resp:
        async with aiofiles.open(f'wallpaper4/{name}','wb') as fp:
            await fp.write(await resp.content.read())
    print(f'正在下载{name}')

async def download(list):
    taks = []
    async with aiohttp.ClientSession() as session:
        for url in list:
            name = url.split('/')[-1]
            f = asyncio.create_task(requ(url,session,name))
            taks.append(f)
        await asyncio.wait(taks)





if __name__ == '__main__':
    ks = time.time()
    with open('ip.txt','r')as f:
        content = f.read()
        proxies = json.loads(content)
    print(len(proxies))
    proxy = random.choice(proxies)

    # 获取hot页面url
    hot_url = []
    for p in range(10,20):
        url = f'https://wallhaven.cc/hot?page={p}'
        hot_url.append(url)
    print(hot_url)
    # 获取page页面url
    page_url = []
    # proxy = random.choice(bpool)
    for h_url in hot_url:
        try:
            resp = requests.get(h_url,headers=headers,proxies=proxy,timeout=1)
            e = etree.HTML(resp.text)
            tree = e.xpath('//figure/a/@href')
            for i in tree:
                page_url.append(i)
                print('正在追加1')
        except:
            print('追加失败')
    print(f'pageurl个数为{len(page_url)}')
    # 获取img_url
    img_url = []
    for i_url in page_url:
        try:
            resp = requests.get(i_url,headers=headers,proxies=proxy,timeout=1)
            e = etree.HTML(resp.text)
            tree = e.xpath('//div/img/@src')
            for i in tree:
                img_url.append(i)
                print('正在追加2')
        except:
            print('追加失败')

    # 下载图片

    asyncio.run(download(img_url))
    js = time.time()
    print(ks-js )

