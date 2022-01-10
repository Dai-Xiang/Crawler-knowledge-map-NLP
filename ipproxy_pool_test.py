# IP地址取自国内髙匿代理IP网站：http://www.ip3366.net/
# 仅仅爬取首页IP地址就足够一般使用
from bs4 import BeautifulSoup
import requests
import random
url_ip = ["http://www.data5u.com/vipip/dynamic.html"]
headers_ip = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60'}


def get_ip_list(url_ip1, headers_ip1):
    web_data = requests.get(url_ip1, headers_ip1)
    web_data.encoding = 'utf-8'
    soup = BeautifulSoup(web_data.text, 'lxml')
    print(soup)
    ips = soup.select('ul[class="l2"]')
    ip_list1 = []
    for i in ips:
        ip_temp = []
        if len(i.select('span')) > 4:
            ip_address = i.select('span')[0].get_text()
            ip_port = i.select('span')[1].get_text()
            # ip_style = i.select('span')[2].get_text()
            # ip_type = i.select('span')[3].get_text()
            # if ip_style == '透明' or ip_type == 'http':
            #     continue
            ip_temp.append(ip_address)
            ip_temp.append(ip_port)
            ip_list1.append(ip_temp)
    return ip_list1


def check_proxy(ip_list1, headers_ip1):
    temp = []
    for i in ip_list1:
        print(i)
        ip1 = i[0]
        port1 = i[1]
        proxy = {"http": "http://" + ip1 + ":" + port1, "https": "https://" + ip1 + ":" + port1}
        try:
            data = requests.get(url="https://movie.douban.com/top250", headers=headers_ip1, proxies=proxy, timeout=5)
            print(data.text)
        except Exception as e:
            print(f"请求失败，代理IP无效！{e}")
        else:
            print("请求成功，代理IP有效！")
            temp.append(i)
    return temp


def get_random_ip(ip_list1):
    proxy_list = []
    if len(ip_list1) == 0:
        return 0
    for ip1 in ip_list1:
        proxy_list.append('https://' + ip1[0] + ':' + ip1[1])
    proxy_ip = random.choice(proxy_list)
    proxies = {'https': proxy_ip}
    return proxies


a = 0
# while a == 0:
ip_lists = []
for url1 in url_ip:
    print(1)
    temp_list = get_ip_list(url1, headers_ip)
    ip_lists.extend(temp_list)
ip_lists = check_proxy(ip_lists, headers_ip)
a = get_random_ip(ip_lists)
print(a)
