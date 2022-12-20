import requests
import random
import json
import time
from concurrent.futures import ThreadPoolExecutor
import re
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.56'
}


def proxies_get():
    with open('ip1.txt','r')as f:
        content = f.read()
        proxies = json.loads(content)
    print(len(proxies))
    return proxies

def hot_get():
    n = input('想要抓取的页码')
    hot_url = []
    for p in range(1,int(n)):
        url = f'https://wallhaven.cc/hot?page={p}'
        hot_url.append(url)
    print('正在下载',hot_url)
    return hot_url,int(n)


def page_url_get(proxies,page_url,h_url):
    # try:
        resp = requests.get(h_url,headers=headers,proxies=random.choice(proxies),timeout=1)
        if resp.status_code == 200:
            src = re.findall(r'data-src="(.*?)"', resp.text)
            for i in src:
                page_url.append(i)
                print('正在追加1')
            print(f'pageurl个数为{len(page_url)}')
            return page_url
    # except:
        else:
            print('追加失败')
            time.sleep(1)
            return page_url_get(proxies,page_url,h_url)



def page_url_thget(hot_url,proxies):
    page_url = []
    with ThreadPoolExecutor(5)as f:
        for h_url in hot_url:
            f.submit(page_url_get,proxies,page_url = page_url,h_url = h_url)
    print(page_url)
    return page_url

def page_url_change(page_url):
    i_url = []
    for url in page_url:
        url_sp = url.split('/')[-1]
        url_data = 'wallhaven-'+url_sp
        url_img = url.replace('th','w').replace('small','full').replace(url_sp,url_data)
        i_url.append(url_img)
        # print(url_img)
    print('i_url num:',len(i_url))
    return i_url


def fn(i,url,proxies):
    # try:
    resp = requests.get(i,proxies=random.choice(proxies),headers=headers,timeout=10)
    if resp.status_code == 404:
        filename = i.replace('.jpg', '.png').split('/')[-1]
    #     try:
        resp = requests.get(i.replace('.jpg', '.png'),proxies=random.choice(proxies),headers=headers,timeout=10)
        with open(f'wallpaper4/{filename}','wb') as f:
            f.write(resp.content)
        print('正在下载',i.replace('.jpg', '.png'))
        url.append(i.replace('.jpg', '.png'))
        return url
    #     except:
    #         print('下载失败',i.replace('.jpg', '.png'))
    #     # print(404)
    elif resp.status_code == 200:
        filename = i.split('/')[-1]
        with open(f'wallpaper4/{filename}','wb') as f:
            f.write(resp.content)
        url.append(i)
        print('正在下载',i)
        return url
    else:
        print('_________________', i)
        time.sleep(5)
        return fn(i,url,proxies)


def img_url_download(page_url,proxies,n):
    with ThreadPoolExecutor(n) as f:
        img_url = []
        # too_requ_url = []
        for i in page_url:
            f.submit(fn,i,img_url,proxies)
    print(len(img_url),'==============')
    return img_url

# def download_img(img,proxie):
#     try:
#         resp = requests.get(img, proxies=random.choice(proxie), headers=headers,timeout=15)
#         filename = img.split('/')[-1]
#         with open(f'wallpaper4/{filename}','wb') as f:
#             f.write(resp.content)
#         print(f'正在下载图片{filename}')
#     except:
#         print('下载失败')
#
# def th_download_img(img_url,proxies,n):
#     with ThreadPoolExecutor(n)as s:
#         for img in img_url:
#             s.submit(download_img,img,proxies)



def main():
    ks = time.time()
    proxies = proxies_get()
    hot_url,n = hot_get()
    print(n)
    page_url = page_url_thget(hot_url,proxies)
    i_url = page_url_change(page_url)
    img_url_download(i_url,proxies,n)
    # th_download_img(img_url,proxies,n)
    js = time.time()
    print(ks - js)

if __name__ == '__main__':
    main()