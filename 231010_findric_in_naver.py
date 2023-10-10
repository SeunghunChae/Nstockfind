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

temp=[]
company=[]
error=[]
output=[]
korea=[]
no_exist=[]
normal=[]

file=open('231010.dat', 'r')

while True :
    line=file.readline()
    if len(line)==0:
        break
    line=line.lstrip()
    line=line.rstrip()
    templine=line.split()
    temp.append(templine)

file.close()

for i in temp:
    company.append(i[0].split('.'))


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

##################### 크롤링 시작 #####################
driver = webdriver.Chrome('c:\chromedriver.exe')
url='https://m.stock.naver.com/search'
for i in range(len(company)):
    print(i)
    lineout=[]
    lineout.append(company[i][0])
    if len(company[i])>1:
        lineout.append(company[i][1])
    else:
        lineout.append("없음")
    name=''
    code=''
    market=''
    k=1    #elem_name1에서 사용

    driver.get(url)
    time.sleep(1)
    inputbox=driver.find_element(By.CSS_SELECTOR, tag_inputbox)
    inputbox.send_keys(company[i][0]) #ric를 떼어냄
    time.sleep(0.5)
    ##검색 결과가 여러개 나오는 경우
    if is_element_present(driver, By.CSS_SELECTOR,elem_name1):  #첫번째 요소로 확인 후 한 개의 경우로 넘어감
        while True:
            elem_name1='#content > div > ul > li:nth-child('+str(k)+') > div.SearchList_link__zBlL1 > strong'
            elem_code1='#content > div > ul > li:nth-child('+str(k)+') > div.SearchList_link__zBlL1 > span > span.SearchList_code__59hG9'
            elem_market1='#content > div > ul > li:nth-child('+str(k)+') > div.SearchList_link__zBlL1 > span > span.SearchList_market__ASMay'
            if is_element_present(driver, By.CSS_SELECTOR,elem_name1):
                target=driver.find_element(By.CSS_SELECTOR, elem_name1)
                name=target.text
                if name==company[i][0]:
                    target=driver.find_element(By.CSS_SELECTOR,elem_code1)
                    code=target.text
                    target=driver.find_element(By.CSS_SELECTOR,elem_market1)
                    market=target.text
                    lineout.append(name)
                    lineout.append(code)
                    lineout.append(market)
                    output.append(lineout)
                    break
                k+=1
            #ric 검색 결과가 여러개가 나왔으나 아무것도 못찾음
            else:                
                break
            if name=='':
                lineout.append("없음")
                lineout.append("없음")
                lineout.append("없음")
                output.append(lineout)
    ##검색결과가 하나만 나오는 경우
    else :
        if is_element_present(driver, By.CSS_SELECTOR,elem_name2):
            target=driver.find_element(By.CSS_SELECTOR,elem_code2)
            code=target.text
            target=driver.find_element(By.CSS_SELECTOR,elem_name2)
            name=target.text
            target=driver.find_element(By.CSS_SELECTOR,elem_market2)
            market=target.text
        else:   ##아예 아무것도 없음
            code="없음"
            name="없음"
            market="없음"
        lineout.append(name)
        lineout.append(code)
        lineout.append(market)
        output.append(lineout)
            
    time.sleep(2)
    inputbox.clear()
file=open('output.csv', 'w')
file.write('DB_NAME,DB_MARKET,NAME,DESC,MARKET\n')
for line in output:
    for token in line:
        file.write(token)
        file.write(',')
    file.write('\n')
file.close()
