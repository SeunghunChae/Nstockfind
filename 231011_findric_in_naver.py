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

import traceback

def check_text(driver, target):
    try:  
        name=target.text
        return True
    except Exception:
        return False
    
def is_element_present(driver, by, value):
    try:
        driver.find_element(by=by, value=value)
        return True
    except Exception:
        return False

def find_tab_statement(driver):
    code1='#_main_stock_tab > div > ul > li:nth-child('
    code2=') > a > span'
    try :        
        for i in range(1,6):
            target=code1+str(i)+code2
            elements=driver.find_element(By.CSS_SELECTOR,target)
            if elements.text=='재무':
                
                return target
    except :
        print('재무항목이 없습니다.')
        return ''

name=[]
company=[]
output=[]
urls=[]

file=open('231010.dat', 'r')

while True :
    line=file.readline()
    if len(line)==0:
        break
    line=line.lstrip()
    line=line.rstrip()
    templine=line.split()
    company.append(templine)

file.close()

for i in company:
    urls.append('https://m.stock.naver.com/worldstock/stock/'+i[0]+'/total')

for i in company:
    name.append(i[0].split('.'))

k=1
#태그를 상수로 정의함
tag_inputbox='#__next > div.SearchBar_article__XF6AA > div > div > div > div > input.SearchBar_input__t2ws8'
elem_name1='#content > div > ul > li:nth-child('+str(k)+') > div.SearchList_link__zBlL1 > strong'
#elem_code1='#content > div > ul > li:nth-child('+str(k)+') > div.SearchList_link__zBlL1 > span > span.SearchList_code__59hG9'
#elem_market1='#content > div > ul > li:nth-child('+str(k)+') > div.SearchList_link__zBlL1 > span > span.SearchList_market__ASMay'
#검색 결과가 하나밖에 없을 경우
elem_name2='#content > div.SearchList_article__v7J3E > ul > li > div.SearchList_link__zBlL1 > strong'
elem_code2='#content > div.SearchList_article__v7J3E > ul > li > div.SearchList_link__zBlL1 > span > span.SearchList_code__59hG9'
elem_market2='#content > div.SearchList_article__v7J3E > ul > li > div.SearchList_link__zBlL1 > span > span.SearchList_market__ASMay'

ric='#content > div.GraphMain_mainGraph__3npcJ.UNCHANGED > div.GraphMain_frameGraph__19k0w > div.GraphMain_stockInfo__2-Uf6 > span.GraphMain_code__2jycd'
close_btn='#BOTTOM_MODAL_NOTICE > button > svg'
check='#content > div.LayoutCard_article__27nL4.favorite_section > div.LayoutCard_box_title__qKnnu > h2'

driver = webdriver.Chrome('c:\chromedriver.exe')
for i in range(1000):
    line=[]
    
    #항목 별 db_ric 정보 입력
    line.append(name[i][0])
    if len(name[i])>1:
        line.append(name[i][1])
    else :
        line.append('없음')    
    
    driver.get(urls[i])
    time.sleep(1.5)

    #팝업창 끄기
    #target=driver.find_element(By.CSS_SELECTOR, close_btn)
    #target.click()

    if is_element_present(driver, By.CSS_SELECTOR,ric):
        #이름가져오기
        target=driver.find_element(By.CSS_SELECTOR, ric)
        name_market=target.text    

        #검색된 이름 중 db_ric 포함여부 확인
        if name_market.find(name[i][0])==0:
            line.append(name[i][0])                     #db_ric name 입력
            line.append(name_market[len(name[i][0]):])  #거래소 이름 입력
        else :
            line.append('확인필요')
            line.append('확인필요')
    else:
        if driver.find_element(By.CSS_SELECTOR, check).text=='관심종목':
            line.append('없음')
            line.append('없음')
        else:
            line.append('확인필요2')
            line.append('확인필요2')
    output.append(line)

file=open('output_1011.csv', 'w')
file.write('DB_NAME,DB_MARKET,NAME,MARKET\n')
for line in output:
    for token in line:
        file.write(token)
        file.write(',')
    file.write('\n')
file.close()
