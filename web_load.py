import requests
import time
from bs4 import BeautifulSoup
import re


# load函数用来下载网页内容，并以字符串形式保存在本地
#请求网页数据，并将其下载到本地的网页数据库。
def load(url1, headers1, temp, proxy1):
    # time.sleep(4)
    response1 = requests.get(url1, headers=headers1, proxies={"http": "http://{}".format(proxy1)})
    response1.encoding = 'utf-8'
    path = 'database/' + temp + '.html'
    # print("len={}".format(len(response1.text)))
    f1 = open(path, 'w', encoding='utf-8')
    f1.write(response1.text)
    f1.close()
    return len(response1.text)
