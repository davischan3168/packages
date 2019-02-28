import requests
import json

import xueqiu.cons as cons
import xueqiu.token as token
from util.chrome_cookies import FetchCookiesFB
from webdata.util.hds import user_agent as hds
#s=requests.Session()

def fetch(url,browser='firefox'):
    """
    HEADERS = {'Host': 'stock.xueqiu.com',
               'Accept': 'application/json',
               'Cookie': token.get_token(),
               'User-Agent': 'Xueqiu iPhone 11.8',
               'Accept-Language': 'zh-Hans-CN;q=1, ja-JP;q=0.9',
               'Accept-Encoding': 'br, gzip, deflate',
               'Connection': 'keep-alive'}
    """

    response = requests.get(url,headers=hds(),cookies=FetchCookiesFB(url,browser=browser))
    #response = s.get(url,headers=hds(),cookies=FetchCookiesFB(url,browser=bowser))
    # print(url)
    # print(HEADERS)
    print(response)
    # print(response.content)

    if response.status_code != 200:
        raise Exception(response.content)

    return json.loads(response.content)


def fetch_without_token(url):
    HEADERS = {'Host': 'stock.xueqiu.com',
               'Accept': 'application/json',
               'User-Agent': 'Xueqiu iPhone 11.8',
               'Accept-Language': 'zh-Hans-CN;q=1, ja-JP;q=0.9',
               'Accept-Encoding': 'br, gzip, deflate',
               'Connection': 'keep-alive'}

    response = requests.get(url, headers=HEADERS)

    # print(url)
    # print(HEADERS)
    # print(response)
    # print(response.content)

    if response.status_code != 200:
        raise Exception(response.content)

    return json.loads(response.content)
