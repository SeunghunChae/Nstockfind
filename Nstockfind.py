from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

from datetime import datetime

import re

import requests

import time
import csv
import chromedriver_autoinstaller


company=[]
search=[]
text=[]
error=[]
output=[]

####################################검색 리스트 입력#######################################

file=open('input.dat', 'r')

while True :
    line=file.readline()
    if len(line)==0:
        break
    line=line.lstrip()
    line=line.rstrip()
    company.append(line)

del company[0]

####################################크롤링 시작#######################################
#chromedriver_autoinstaller.install()    #크롬 버전업 문제방지
options = webdriver.ChromeOptions()
##options.add_argument('--headless')
##options.add_argument('--disable-gpu')
service = Service('c:\chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)

url='https://m.stock.naver.com/search'

for i in range(1033,1035):
    print(i)
    content=''
    name=''
    flag=0
    try:
        driver.get(url)

        inputbox=driver.find_element(By.CSS_SELECTOR, '#__next > div.ViewportFrame_article__KgZKu > div.SearchBar_article__XF6AA > div > div > div > input.SearchBar_input__t2ws8')
        inputbox.send_keys(company[i])                      #글자입력
        #inputbox.send_keys(Keys.CONTROL, 'a')              #글자지우기
        #inputbox.send_keys(Keys.DELETE)
        #inputbox.send_keys(Keys.ENTER)
        time.sleep(0.5)

        target=driver.find_element(By.CSS_SELECTOR,'#__next > div.ViewportFrame_article__KgZKu > div.SearchList_article__v7J3E > ul > li:nth-child(1) > div.SearchList_link__zBlL1 > strong > em')
        code=target.text
        target=driver.find_element(By.CSS_SELECTOR,'#__next > div.ViewportFrame_article__KgZKu > div.SearchList_article__v7J3E > ul > li:nth-child(1) > div.SearchList_link__zBlL1 > span > span.SearchList_code__59hG9')     
        name=target.text
        print((code,name))
        target.click()

        #기업 페이지 들어옴. 기업개요 버튼 뜰때까지 기다림
        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#_main_stock_tab > div > ul > li:nth-child(6) > a > span')))    
        overview=driver.find_element(By.CSS_SELECTOR,"#_main_stock_tab > div > ul > li:nth-child(6) > a > span")
        overview.click()

        try:
            #기업개요 뜰때까지 기다림
            WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#content > div.OverviewContainer_overviewContainer__2Gzn5 > div.OverviewContainer_infoCorp__3K5qX')))    
            comp=driver.find_element(By.CSS_SELECTOR,"#content > div.OverviewContainer_overviewContainer__2Gzn5 > div.OverviewContainer_infoCorp__3K5qX")
            content=comp.text.replace('\n','').replace(',','')
            print(content)
            #__next > div.ViewportFrame_article__KgZKu > div.SearchList_article__v7J3E > ul > li:nth-child(1)
            #__next > div.ViewportFrame_article__KgZKu > div.SearchList_article__v7J3E > ul > li:nth-child(1) > div.SearchList_link__zBlL1 > strong > em
            flag=1
            search.append((code,name,content))
            
        except Exception:
            comp=driver.find_element(By.CSS_SELECTOR,"#content > div.OverviewContainer_overviewContainer__2Gzn5 > div.NewError_article__2j3to > strong")
            print(comp.text)
            if '잠시 후 다시 시도해 주세요' in comp.text:
                output.append((i, code, name))
            flag=1
            
        finally:
            if flag !=1:
                error.append(i,content)
            
    except Exception:
        error.append((i,content,name))  #etf는 에러가 난다 => 기업 개요가 없다.


with open('정상.csv','a',newline='') as f:
    f.write('코드,기업명,내용,')
    f.write('\r\n')
    for i in search :
        line=i[0]+','+i[1]+','+i[2]
        f.write(line)
        f.write('\r\n')


with open('누락목록.csv','a',newline='') as f:
    f.write('i,내용,')
    f.write('\r\n')
    for i in output :
        line=str(i[0])+','+i[1]
        f.write(line)
        f.write('\r\n')


with open('에러.csv','a',newline='') as f:
    f.write('etf,i,내용,이름,')
    f.write('\r\n')
    for i in error :
        line=str(i[0])+','+i[1]+','+i[2]
        if 'etf' in i[2].lower():
            line+='etf,'+line
        else:
            line=','+line
        f.write(line)
        f.write('\r\n')
