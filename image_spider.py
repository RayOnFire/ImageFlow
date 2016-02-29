from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
import urllib.request as request
import urllib.error
import socket
import json

def get_content():
    driver = webdriver.PhantomJS()
    driver.get('http://www.pixiv.net/ranking.php?mode=daily')
    height = driver.execute_script(" return document.body.scrollHeight")
    print(height)
    scroll_top = 0
    while scroll_top < height:
        driver.execute_script("window.scrollTo(0, %d)" % scroll_top)
        scroll_top += 20
        height = driver.execute_script(" return document.body.scrollHeight")
        print(height)
        if height > 200000:
            break
    data = driver.find_element(By.ID, 'wrapper')
    return data.get_attribute('innerHTML')

def construct_only(url):
    new = []
    new.append(url[:20])
    new.append('img-original/img/')
    new.append(url[45:76])
    new.append('.jpg')
    new = ''.join(new)
    return new

def construct_url(url, referer):
    new = []
    new.append(url[:20])
    new.append('img-original/img/')
    new.append(url[45:76])
    new.append('.jpg')
    new = ''.join(new)
    print(new)
    return request.Request(new, headers={'referer': referer})
    

with open('test.html', 'wb') as f:
    f.write(bytes(get_content(), 'utf-8'))

PREFIX = 'http://www.pixiv.net/'
with open('test.html', 'rb') as f:
    content = f.read().decode()
bs = BeautifulSoup(content, 'html.parser')
a = bs.find_all('img')
li = [x['src'] for x in a]
b = bs.find_all(class_='work')
refer_li = [PREFIX + x['href'] for x in b]
li2 = []
for i in li:
    if not 'source' in i and not 'profile' in i:
        li2.append(i)
li3 = []
for i in li2:
    li3.append(construct_only(i))
obj_li = []
obj = {}
for i in range(len(li3)):
    obj['id'] = i
    obj['referer'] = refer_li[i]
    obj['src'] = li3[i]
    obj_li.append(obj)
    obj = {}
with open('original.json', 'w') as f:
    f.write(json.dumps(obj_li));

for i in range(len(li2)):
    with open('img/' + li2[i][65:], 'wb') as f:
        try:
            url = construct_url(li2[i], refer_li[i])
            f.write(request.urlopen(url, timeout=10).read())
        except urllib.error.HTTPError:
            print('HttpError')
        except socket.timeout:
            print('timeout')

#driver = webdriver.PhantomJS()
#driver.get(PREFIX + li[0])
#data = driver.find_element(By.ID, 'wrapper')
#data = data.get_attribute('innerHTML')
#c = request.urlopen(PREFIX + li[0])
#with open('test2.txt', 'wb') as f:
#    f.write(bytes(data, 'utf-8'))
#bs = BeautifulSoup(c.read(), 'html.parser')
#a = bs.find(class_='_illust_modal')
#print(len(a))
'''
for i in li2:
    with open('img/' + i[65:], 'wb') as f:
        content = request.urlopen(i).read()
        with open('test2.txt', 'wb') as f:
            f.write(content.decode())
        bs = BeautifulSoup(content, 'html.parser')
        a = bs.find(class_='_illust_modal')
        print(a['data-src'])
'''
#http://i1.pixiv.net/img-original/img/2016/02/24/07/44/31/55459612_p0.jpg
#http://i1.pixiv.net/c/240x480/img-master/img/2016/02/24/07/44/31/55459612_p0_master1200.jpg