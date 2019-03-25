# coding: utf-8

import requests
from bs4 import BeautifulSoup
import multiprocessing
import time

PROCESS_NUM = 32
CRAWL_PAGE_NUM  = 16
TIMES = 10
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Ubuntu Chromium/44.0.2403.89 '
                        'Chrome/44.0.2403.89 '
                        'Safari/537.36'}

LINKS = ["https://blog.csdn.net/marvellousbinary/article/details/79182946",
             'https://blog.csdn.net/marvellousbinary/article/details/80470402',
             'https://blog.csdn.net/marvellousbinary/article/details/80144329',
             'https://blog.csdn.net/marvellousbinary/article/details/80527189',
             'https://blog.csdn.net/marvellousbinary/article/details/80634597',
             'https://blog.csdn.net/marvellousbinary/article/details/80689517',
             'https://blog.csdn.net/marvellousbinary/article/details/79797694',
             'https://blog.csdn.net/marvellousbinary/article/details/79832708',
             ]

def getProxyIp():
    proxies = []
    for i in range(1, CRAWL_PAGE_NUM):
        r = requests.get('http://www.xicidaili.com/nt/{0}'.format(i), headers=HEADERS)
        soup = BeautifulSoup(r.text,"lxml")
        table = soup.find('table', attrs={'id': 'ip_list'})
        tr = table.find_all('tr')[1:]

        # 解析得到代理ip的地址，端口，和类型
        for item in tr:
            tds = item.find_all('td')
            # print( tds[1].get_text())          ip
            http_ip = "http://{0}:{1}".format(tds[1].get_text(), tds[2].get_text())
            https_ip = "https://{0}:{1}".format(tds[1].get_text(), tds[2].get_text())
            iptype = tds[5].get_text().lower()  # http or https
            if 'https'  == iptype:
                ip = "https://{0}:{1}".format(tds[1].get_text(), tds[2].get_text())
                proxies.append({'https':ip})
    return proxies

def brush(proxy_dict):
    fail_time = 0
    for link in LINKS:
        try:
            r = requests.get(link,headers=HEADERS, proxies=proxy_dict, timeout=10)
        except Exception as e:
            #print(e)
            print('fail')
            fail_time +=1
    time.sleep(0.5)

def genProc(proxies,n = PROCESS_NUM):
    if n>PROCESS_NUM or n!=len(proxies): n = min(PROCESS_NUM, n, len(proxies))
    pool = multiprocessing.Pool(processes=n)
    results = [pool.apply_async(brush, (proxies[i],)) for i in range(n)]
    for i in range(n): results[i].get()
    pool.close()
    pool.join()

if __name__ == '__main__':  
    for _ in range(TIMES):
        proxies = getProxyIp()
        ct = len(proxies)
        while ct > PROCESS_NUM:
            genProc(proxies[ct-PROCESS_NUM:ct],PROCESS_NUM)
            ct -= PROCESS_NUM
        genProc(proxies[:ct], ct)
