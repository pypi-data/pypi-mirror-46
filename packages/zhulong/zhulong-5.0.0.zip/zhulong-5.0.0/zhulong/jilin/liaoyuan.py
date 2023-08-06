import time

import pandas as pd
import re

from selenium import webdriver
from bs4 import BeautifulSoup
from lmf.dbv2 import db_write
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import json

from zhulong.util.etl import est_tbs,est_meta,est_html

# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]

#
# url="http://www.ccggzy.gov.cn/qxxxgk/003002/003002004/CountyPurhcaseNotice.html"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)
#

_name_='liaoyuan'


def f1(driver,num):
    locator = (By.XPATH, '//ul[@class="ly_list"]/li[1]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    url=driver.current_url

    if 'index.html' in url:
        cnum = 1
    else:
        cnum = re.findall('index_(\d+).html', url)[0]
        cnum = int(cnum) + 1

    if cnum != num:
        if num == 1:
            url=url.rsplit('/', maxsplit=1)[0] + '/index.html'
        else:
            url = url.rsplit('/', maxsplit=1)[0] + '/index_' + str(num-1) + '.html'

        val = driver.find_element_by_xpath('//ul[@class="ly_list"]/li[1]/a').get_attribute('href')[-25:-5]
        driver.get(url)
        locator = (By.XPATH, '//ul[@class="ly_list"]/li[1]/a[not(contains(@href,"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    data = []

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find('ul', class_='ly_list')
    trs = div.find_all('li', attrs={'class': ''})

    url = driver.current_url
    main_url = url.rsplit('/', maxsplit=1)[0]
    for tr in trs:

        href = tr.a['href'].strip('.')
        name = tr.a.get_text()
        ggstart_time = tr.span.get_text()

        if 'http' in href:
            href = href
        else:
            href = main_url + href

        tmp = [name, ggstart_time, href]
        data.append(tmp)
    df = pd.DataFrame(data=data)
    df["info"] = None
    return df


def f2(driver):
    locator = (By.XPATH, '//ul[@class="ly_list"]/li[1]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    page = driver.find_element_by_xpath('//div[@class="ly_ggzyjyzx_page_tzgg"]/div[2]/a[last()]').get_attribute('href')
    total = re.findall('index_(\d+).html', page)[0]

    total = int(total) + 1
    driver.quit()

    return total


def f3(driver, url):
    driver.get(url)

    locator = (By.XPATH, '(//div[@class="TRS_Editor"])[1]')

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
    div = soup.find('div', class_='TRS_Editor')
    return div




data=[
    #包含：招标，变更等公告
    ["gcjs_zhaobiao_gg","http://ggzy.liaoyuan.gov.cn/xxgk/zhaobgg/index.html",["name","ggstart_time","href","info"],f1,f2],
    #包含，中标，中标候选，流标公告
    ["gcjs_zhongbiaohx_gg","http://ggzy.liaoyuan.gov.cn/xxgk/zhongbgg/index.html",["name","ggstart_time","href","info"],f1,f2],

]

def work(conp,**args):
    est_meta(conp,data=data,diqu="吉林省辽源市",**args)
    est_html(conp,f=f3,**args)

if __name__=='__main__':


    work(conp=["postgres","since2015","192.168.3.171","jilin","liaoyuan"],headless=False,num=1)