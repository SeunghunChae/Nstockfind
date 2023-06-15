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

class FindKoreaException(Exception): ## Exception을 상속받아야한다.
    def __init__(self):
        super().__init__('한국종목이 나왔습니다.') 

class TimeoutException(Exception): ## while이 3초 이상 돌 경우
    def __init__(self,timeout):
        super().__init__(f"while이 {timeout} 초 이상 돌았습니다.")

class NotEtfException(Exception): ## while이 3초 이상 돌 경우
    def __init__(self,name):
        super().__init__(f"{name}는 etf가 아닙니다.")

company=[]
etf=[]
error=[]
output=[]
korea=[]
no_exist=[]

file=open('input.dat', 'r')
idx_etf=open('etf.dat', 'r')

while True :
    line=file.readline()
    if len(line)==0:
        break
    line=line.lstrip()
    line=line.rstrip()
    company.append(line)

del company[0]
file.close()

while True :
    line=idx_etf.readline()
    if len(line)==0:
        break
    line=line.lstrip()
    line=line.rstrip()
    etf.append(int(line))
idx_etf.close()

k=1
elem_name1='#__next > div.ViewportFrame_article__KgZKu > div.SearchList_article__v7J3E > ul > li:nth-child('+str(k)+') > div.SearchList_link__zBlL1 > strong'
elem_code1='#__next > div.ViewportFrame_article__KgZKu > div.SearchList_article__v7J3E > ul > li:nth-child('+str(k)+') > div.SearchList_link__zBlL1 > span > span.SearchList_code__59hG9'
elem_market1='#__next > div.ViewportFrame_article__KgZKu > div.SearchList_article__v7J3E > ul > li:nth-child('+str(k)+') > div.SearchList_link__zBlL1 > span > span.SearchList_market__ASMay'

#검색 결과가 하나밖에 없을 경우
elem_name2='#__next > div.ViewportFrame_article__KgZKu > div.SearchList_article__v7J3E > ul > li > div.SearchList_link__zBlL1 > strong'
elem_code12='#__next > div.ViewportFrame_article__KgZKu > div.SearchList_article__v7J3E > ul > li > div.SearchList_link__zBlL1 > span > span.SearchList_code__59hG9'
elem_market2='#__next > div.ViewportFrame_article__KgZKu > div.SearchList_article__v7J3E > ul > li > div.SearchList_link__zBlL1 > span > span.SearchList_market__ASMay'

elem_overview1='#content > div.Overview_article__3sC9o.Overview_articleIndex__2m4YI > div'

check_etf='#content > div.Overview_article__3sC9o.Overview_articleIndex__2m4YI > strong'

##################### 크롤링 시작 #####################
driver = webdriver.Chrome()

url='https://m.stock.naver.com/search'
for i in range(0,len(etf)):
    print(i)    
    idx=etf[i]
    name=''
    code=''
    market=''
    k=1
    
    try:
        driver.get(url)
        time.sleep(0.5)
        inputbox=driver.find_element(By.CSS_SELECTOR, '#__next > div.ViewportFrame_article__KgZKu > div.SearchBar_article__XF6AA > div > div > div > input.SearchBar_input__t2ws8')
        inputbox.send_keys(company[idx])
        time.sleep(0.5)
        #이름을 찾는다
        time.sleep(0.5)
        if is_element_present(driver, By.CSS_SELECTOR,elem_name1):
            target=driver.find_element(By.CSS_SELECTOR, elem_name1)
            name=target.text
            start_time = time.time() # 3초 이상 걸리면 탈출
            while True: #한국종목일경우 코드번호를 통해 미국 종목을 찾는다.
                elapsed_time = time.time() - start_time
                if elapsed_time>3:
                    raise TimeoutException('3')
                target=driver.find_element(By.CSS_SELECTOR, elem_code1)
                start_time2 = time.time() # 3초 이상 걸리면 탈출
                while True: #로딩이 늦어 em이 안읽혔을때 여기가 읽히는 경우가 있다. 이 경우 text를 가져올 수 없어 exception을 뿜는다. 확인 후 진행하는 코드 추가
                    elapsed_time2 = time.time() - start_time2
                    if elapsed_time2>3:
                        raise TimeoutException('3')
                    if check_text(driver,target):
                        code=target.text
                        target=driver.find_element(By.CSS_SELECTOR, elem_market1)
                        market=target.text
                        if code.isdigit(): #한국종목 발견
                            raise FindKoreaException
                        code, name = name, code #미국종목은 한국종목과 code, name이 반대이다.
                        target.click()
                        break
                k+=1
                if len(code)!=0:
                    break
        else :
            target=driver.find_element(By.CSS_SELECTOR,elem_code2)
            code=target.text
            target=driver.find_element(By.CSS_SELECTOR,elem_name2)
            name=target.text
            target=driver.find_element(By.CSS_SELECTOR,elem_market2)
            market=target.text
            target.click()

        print(code+' '+name+' '+market)
        ###########################기업 페이지 들어옴###################################
        start_time = time.time()
        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time>3:
                raise NotEtfException(company[idx])
            if is_element_present(driver, By.CSS_SELECTOR,check_etf): #기업 개요가 나올때까지 기다린다
                if is_element_present(driver, By.CSS_SELECTOR,elem_overview1):
                    overview=driver.find_element(By.CSS_SELECTOR,elem_overview1).text
                    output.append((idx, code, name, market, overview))
                    break
                else :
                    no_exist.append((idx, code, name, market))
                    break

        

    except FindKoreaException as e:
        korea.append((idx, code, name,market))
        print("korea : "+str(idx)+' '+code+' '+name)
        print(e)

    except TimeoutException as e:
        code_err=traceback.format_exc()
        no=re.search(r'line (\d+)',code_err)
        error.append((i,code, name, market,'Timeout'))
        print(str(i)+'에서 오류발생 , '+no.group()+' :')
        print(str(e))

    except NotEtfException as e:
        error.append((i,code, name, market,'not etf'))
        print(str(e))
        
    except Exception as e:   #에러목록 수집
        code_err=traceback.format_exc()
        no=re.search(r'line (\d+)',code_err)
        error.append((i,code, name, market,'unknown error'))
        print(no.group()+' 에서 에러발생함. 일반 에러출력')
        
with open('etf.csv','a',newline='') as f:
    f.write('i,코드,상품명,거래소,개요,')
    f.write('\r\n')
    for i in output :
        line=''
        line=str(i[0])+','+i[1]+','+i[2]+','+i[3]+','+i[4]
        f.write(line)
        f.write('\r\n')

with open('etf_missing.csv','a',newline='') as f:
    f.write('i,코드,상품명,거래소,')
    f.write('\r\n')
    for i in no_exist :
        line=''
        line=str(i[0])+','+i[1]+','+i[2]+','+i[3]
        f.write(line)
        f.write('\r\n')

with open('error.csv','a',newline='') as f:
    f.write('i,코드,상품명,거래소,error')
    f.write('\r\n')
    for i in error :
        line=''
        line=str(i[0])+','+i[1]+','+i[2]+','+i[3]+','+i[4]
        f.write(line)
        f.write('\r\n')
