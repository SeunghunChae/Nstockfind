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

def is_element_present(driver, by, value):
    try:
        driver.find_element(by=by, value=value)
        return True
    except Exception:
        return False

def check_text(driver, target):
    try:
        target=driver.find_element(By.CSS_SELECTOR,'#__next > div.ViewportFrame_article__KgZKu > div.SearchList_article__v7J3E > ul > li:nth-child('+str(k)+') > div.SearchList_link__zBlL1 > span > span.SearchList_code__59hG9')     
        name=target.text
        return True
    except Exception:
        return False                


company=[]
search=[]
text=[]
error=[]
output=[]
korea=[]

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
#크롤링 차단 방지 user-agent 추가 
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36")
service = Service('c:\chromedriver.exe')
driver = webdriver.Chrome()

url='https://m.stock.naver.com/search'

for i in range(9000,len(company)):
    print(i)
    content=''
    name=''
    flag=0
    try:
        driver.get(url)
        time.sleep(0.5)

        inputbox=driver.find_element(By.CSS_SELECTOR, '#__next > div.ViewportFrame_article__KgZKu > div.SearchBar_article__XF6AA > div > div > div > input.SearchBar_input__t2ws8')
        inputbox.send_keys(company[i])                      #글자입력
        #inputbox.send_keys(Keys.CONTROL, 'a')              #글자지우기
        #inputbox.send_keys(Keys.DELETE)
        #inputbox.send_keys(Keys.ENTER)
        time.sleep(0.7)

        #################################회사명 검색###################################
        #가끔씩 child가 없는 경우가 있음
        if is_element_present(driver, By.CSS_SELECTOR, '#__next > div.ViewportFrame_article__KgZKu > div.SearchList_article__v7J3E > ul > li:nth-child(1) > div.SearchList_link__zBlL1 > strong > em'):
            k=1
            while True:
                target=driver.find_element(By.CSS_SELECTOR,'#__next > div.ViewportFrame_article__KgZKu > div.SearchList_article__v7J3E > ul > li:nth-child('+str(k)+') > div.SearchList_link__zBlL1 > span > span.SearchList_code__59hG9')     
                name=target.text
                if name.isdigit() == False:    #미국종목 발견
                    target=driver.find_element(By.CSS_SELECTOR,'#__next > div.ViewportFrame_article__KgZKu > div.SearchList_article__v7J3E > ul > li:nth-child('+str(k)+') > div.SearchList_link__zBlL1 > strong > em')
                    code=target.text           
                    print((code,name))
                    target.click()
                    break
                else : #code가 숫자면 한국 종목이다. 한국종목과 겹치면 무한루프에 빠진다.
                    print(company[i]+' 한국')
                    k+=1
        elif is_element_present(driver, By.CSS_SELECTOR, '#__next > div.ViewportFrame_article__KgZKu > div.SearchList_article__v7J3E > ul > li:nth-child(1) > div.SearchList_link__zBlL1 > strong'):
            k=1
            while True:
                target=driver.find_element(By.CSS_SELECTOR,'#__next > div.ViewportFrame_article__KgZKu > div.SearchList_article__v7J3E > ul > li:nth-child('+str(k)+') > div.SearchList_link__zBlL1 > span > span.SearchList_code__59hG9')     
                name=target.text
                if name.isdigit()!=True:    #미국종목 발견
                    target=driver.find_element(By.CSS_SELECTOR,'#__next > div.ViewportFrame_article__KgZKu > div.SearchList_article__v7J3E > ul > li:nth-child('+str(k)+') > div.SearchList_link__zBlL1 > strong')
                    if check_text(driver,target):   #로딩이 늦어 em이 안읽혔을때 여기가 읽히는 경우가 있다. 이 경우 text를 가져올 수 없어 exception을 뿜는다. 확인 후 진행하는 코드 추가
                        code=target.text           
                        print((code,name))
                        target.click()
                        break
                else : #code가 숫자면 한국 종목이다. 한국종목과 겹치면 무한루프에 빠진다.
                    print(company[i]+' 한국')
                    korea.append((i,company[i]))
                    k+=1
        else:
            target=driver.find_element(By.CSS_SELECTOR,'#__next > div.ViewportFrame_article__KgZKu > div.SearchList_article__v7J3E > ul > li > div.SearchList_link__zBlL1 > strong')
            code=target.text
            target=driver.find_element(By.CSS_SELECTOR,'#__next > div.ViewportFrame_article__KgZKu > div.SearchList_article__v7J3E > ul > li > div.SearchList_link__zBlL1 > span > span.SearchList_code__59hG9')     
            name=target.text
            print((code,name))
            target.click()
            

        ###########################기업 페이지 들어옴################################### 
        time.sleep(0.5)
        if is_element_present(driver, By.CSS_SELECTOR, '#_main_stock_tab > div > ul > li:nth-child(6) > a > span'):
            overview=driver.find_element(By.CSS_SELECTOR,"#_main_stock_tab > div > ul > li:nth-child(6) > a > span")
            overview.click()
        else :
            overview=driver.find_element(By.CSS_SELECTOR,"#_main_stock_tab > div > ul > li:nth-child(5) > a > span")
            overview.click()

        try:
            #기업개요 내용 뜰때까지 기다림
            while True:
                if is_element_present(driver, By.CSS_SELECTOR, '#content > div.OverviewContainer_overviewContainer__2Gzn5 > div.OverviewContainer_infoCorp__3K5qX'):
                    break
                elif is_element_present(driver, By.CSS_SELECTOR, '#content > div.OverviewContainer_overviewContainer__2Gzn5 > div.NewError_article__2j3to > strong'):
                    break
            comp=driver.find_element(By.CSS_SELECTOR,"#content > div.OverviewContainer_overviewContainer__2Gzn5 > div.OverviewContainer_infoCorp__3K5qX")
            content=comp.text.replace('\n','').replace(',','')
            print(content)
            #__next > div.ViewportFrame_article__KgZKu > div.SearchList_article__v7J3E > ul > li:nth-child(1)
            #__next > div.ViewportFrame_article__KgZKu > div.SearchList_article__v7J3E > ul > li:nth-child(1) > div.SearchList_link__zBlL1 > strong > em
            flag=1
            search.append((i,code,name,content))
            
        except Exception:
            comp=driver.find_element(By.CSS_SELECTOR,"#content > div.OverviewContainer_overviewContainer__2Gzn5 > div.NewError_article__2j3to > strong")
            print(comp.text)
            if '잠시 후 다시 시도해 주세요' in comp.text:
                output.append((i, code, name))
            flag=1
            
        finally:    #일반오류로 실행이 안됨
            if flag !=1:
                error.append(i,content,name,code)
            
    except Exception:   #etf는 에러가 난다
        error.append((i,content,name,code))  


with open('정상.csv','a',newline='') as f:
    f.write('i,코드,기업명,내용,')
    f.write('\r\n')
    for i in search :
        line=''
        line=str(i[0])+','+i[1]+','+i[2]+','+i[3]
        f.write(line)
        f.write('\r\n')


with open('누락목록.csv','a',newline='') as f:
    f.write('i,코드,이름,')
    f.write('\r\n')
    for i in output :
        line=''
        line=str(i[0])+','+i[1]+','+i[2]
        f.write(line)
        f.write('\r\n')


with open('에러.csv','a',newline='') as f:
    f.write('i,etf,코드,이름,내용,')
    f.write('\r\n')
    for i in error :
        line=''
        if 'etf' in i[2].lower():
            line=str(i[0])+',etf,'+i[3]+','+i[2]+','+i[1]
        else:
            line=str(i[0])+',,'+i[3]+','+i[2]+','+i[1]
        f.write(line)
        f.write('\r\n')


with open('한국.csv','a',newline='') as f:
    f.write('i,이름,')
    f.write('\r\n')
    for i in korea :
        line=''
        line=str(i[0])+','+i[1]
        f.write(line)
        f.write('\r\n')
