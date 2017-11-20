import urllib.request
import re
import http.cookiejar
import time
import random
import requests
from lxml import html

values = {}
data = urllib.parse.urlencode(values).encode(encoding = 'utf-8')

file1 = open('spider_stocks.txt','r',encoding = 'utf-8')
allstocks = file1.read()
validitems = re.findall('\d{6}',allstocks)
#allurl = []
prices = {}

cookie = http.cookiejar.CookieJar()
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)

headers1 = {#'HOST':'http://gupiao.baidu.com',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
           'Referer':'http://quote.eastmoney.com/stocklist.html',
           'ACCEPT':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'ACCEPT_LANGUAGE':'zh-CN,zh;q=0.8',        
            }

for item in validitems:
    file2 = open('spider_stocks_price2.txt','a',encoding = 'utf-8')
    shurl = "https://gupiao.baidu.com/stock/sh"+item+".html"
    szurl = "https://gupiao.baidu.com/stock/sz"+item+".html"
    time.sleep(1 + random.randrange(30)/100.0)
    response1 = None
    temp = None
    p = None
    try:
        response1 = requests.get(shurl,headers=headers1,timeout = 1)
        temp = html.document_fromstring(response1.text)
        p = temp.xpath('//strong[@class="_close"]')
        prices[item] = p[0].text
    except IndexError as e:
        try:
            response1 = requests.get(szurl,headers=headers1,timeout = 1)
            temp = html.document_fromstring(response1.text)
            p = temp.xpath('//strong[@class="_close"]')
            prices[item] = p[0].text
        except requests.HTTPError as e:
            print(e)
        except IndexError as e:
            prices[item] = "Unknown"
        except:
            continue
        else:
            print('ok')
    except requests.HTTPError as e:
        print(e)
    except:
        continue
    else:
        print('ok')
    
    
    try:
        print(item+' '+prices[item])
        file2.write(item + '\t' + prices[item] + '\n')
    except TypeError as e:
        print(e)
    file2.close()

