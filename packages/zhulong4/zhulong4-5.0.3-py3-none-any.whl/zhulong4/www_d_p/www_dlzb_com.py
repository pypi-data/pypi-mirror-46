from collections import OrderedDict

import pandas as pd
import re

from selenium import webdriver
from bs4 import BeautifulSoup
from lmf.dbv2 import db_write
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json

import time

from zhulong.util.etl import est_html, est_meta, add_info,est_meta_large

_name_ = "www_dlzb_com"


def f1(driver, num):
    locator = (By.XPATH, "//ul[@class='gclist_ul listnew']/li[last()]/a[1]")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    url = driver.current_url
    try:
        cnum = int(driver.find_element_by_xpath("//div[@class='pages']/strong").text.strip())
    except:
        cnum = 1
    if num != int(cnum):
        val = driver.find_element_by_xpath("//ul[@class='gclist_ul listnew']/li[1]/a[1]").get_attribute('href')[-15:]
        tar = driver.find_element_by_xpath("//ul[@class='gclist_ul listnew']/li[last()]/a[1]").get_attribute('href')[-15:]
        if 'page' not in url:
            s = '&page=%d' if num > 1 else "&page=1"
            url +=s
        if num == 1:
            url = re.sub("page=[0-9]*", "page=1", url)
        else:
            s = "page=%d" % (num) if num > 1 else "page=1"
            url = re.sub("page=[0-9]*", s, url)
            # print(cnum)
        driver.get(url)
        time.sleep(1)
        locator = (By.XPATH, "//ul[@class='gclist_ul listnew']/li[1]/a[1][not(contains(@href, '%s'))]" % val)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "//ul[@class='gclist_ul listnew']/li[last()]/a[1][not(contains(@href, '%s'))]" % tar)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))

    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")
    div = soup.find("ul", class_='gclist_ul listnew')
    lis = div.find_all('li')
    data = []
    for li in lis:
        a = li.find("a", class_='gccon_title')
        title = a.text.strip()
        link = a["href"]
        if 'http' in link:
            href = link
        else:
            href = 'https://www.dlzb.com/' + link
        span = li.find("span", class_='gc_date').text.strip()
        tmp = [title, span, href]
        data.append(tmp)
    df = pd.DataFrame(data=data)
    df['info'] = None
    return df



def f2(driver):
    locator = (By.XPATH, "//ul[@class='gclist_ul listnew']/li[1]/a[1]")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        locator = (By.XPATH, "//div[@class='pages']/a[last()-1]")
        num = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
    except:
        num = 1
    driver.quit()
    return int(num)


def f3(driver, url):
    driver.get(url)
    locator = (By.XPATH, "//div[@id='content'][string-length()>40]")
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))

    before = len(driver.page_source)
    time.sleep(0.1)
    after = len(driver.page_source)
    i = 0
    while before != after:
        before = len(driver.page_source)
        time.sleep(0.1)
        after = len(driver.page_source)
        i += 1
        if i > 5: break

    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    div = soup.find('div', class_='text')
    if div == None:
        div = soup.find('div', class_='t_area1')
        if div == None:
            div = soup.find('div', class_='po')
            if div == None:
                div = soup.find('div', id='content')
    return div


def get_data():
    data = []
    # 工程建设部分
    lx = OrderedDict([("gc", "5"), ("hw", "6"), ("fw", "7")])
    ss = OrderedDict([("北京", "1"), ("上海", "2"), ("天津", "3"), ("重庆", "4"), ("河北", "5"),
                      ("山西", "6"), ("内蒙古", "7"), ("辽宁", "8"), ("吉林", "9"), ("黑龙江", "10"),
                       ("江苏", "11"), ("浙江", "12"), ("安徽", "13"), ("福建", "14"), ("江西", "15"),
                       ("山东", "16"), ("河南", "17"), ("湖北", "18"), ("湖南", "19"), ("广东", "20"),
                       ("广西", "21"), ("海南", "22"), ("四川", "23"), ("贵州", "24"), ("云南", "25"),
                       ("西藏", "26"), ("陕西", "27"), ("甘肃", "28"), ("青海", "29"), ("宁夏", "30"), ("新疆", "31")
                       ])

    # 招标
    for w1 in lx.keys():
        for w2 in ss.keys():
            href = "https://www.dlzb.com/zb/search.php?catid=%s&areaid=%s" % (lx[w1], ss[w2])
            tb = "qy_zhaobiao_%s_diqu%s_gg" % (w1, ss[w2])
            col = ["name", "ggstart_time", "href", "info"]
            if w1 == 'gc':
                zblx = '工程招标'
            elif w1 == 'hw':
                zblx = '货物招标'
            elif w1 == 'fw':
                zblx = '服务招标'
            else:zblx=None
            tmp = [tb, href, col, add_info(f1, {"diqu": w2, "zblx":zblx}), f2]
            data.append(tmp)

    # 中标
    for w2 in ss.keys():
        href = "https://www.dlzb.com/zhongbiao/search.php?catid=319&areaid=%s" % (ss[w2])
        tb = "qy_zhongbiao_diqu%s_gg" % (ss[w2])
        col = ["name", "ggstart_time", "href", "info"]
        tmp = [tb, href, col, add_info(f1, {"diqu": w2}), f2]
        data.append(tmp)

    data1 = data.copy()
    remove_arr = []
    for w in data:
        if w[0] in remove_arr: data1.remove(w)
    return data1
    # 创建data

data = get_data()



def work(conp, **args):
    est_meta_large(conp, data=data, diqu="中国电力", **args, interval_page=100)
    est_html(conp, f=f3, **args)


# 该网站需要登录才能看到更多数据，f1数据获取不全，一次性跑不完
if __name__ == '__main__':
    work(conp=["postgres", "since2015", "192.168.3.171", "guoziqiang3", "www_dlzb_com"],pageloadtimeout=180,pageLoadStrategy="none")

    # driver = webdriver.Chrome()
    # url = "https://www.dlzb.com/zb/search.php?catid=6&areaid=2"
    # driver.get(url)
    # df = f2(driver)
    # print(df)
    #
    # driver=webdriver.Chrome()
    # url = "https://www.dlzb.com/zb/search.php?catid=6&areaid=2"
    # driver.get(url)
    # for i in range(13, 15):
    #     df=f1(driver, i)
    #     print(df.values)
