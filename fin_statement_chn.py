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

def check_market(ric, market):
    if ric=='SZ':
        if market.find('선강퉁'):
            return True
    elif ric=='SS':
        if market.find('후강퉁'):
            return True
    else :
        return False

class FindKoreaException(Exception): ## Exception을 상속받아야한다.
    def __init__(self):
        super().__init__('한국종목이 나왔습니다.') 

class TimeoutException(Exception): ## while이 3초 이상 돌 경우
    def __init__(self,timeout):
        super().__init__(f"while이 {timeout} 초 이상 돌았습니다.")

class NoStatementException(Exception): ## while이 3초 이상 돌 경우
    def __init__(self):
        super().__init__(f"재무버튼이 없습니다.")

company=[]
error=[]
output=[]
korea=[]
no_exist=[]
normal=[]

file=open('REFFINSTATEMENTIN_CHN.dat', 'r')

while True :
    line=file.readline()
    if len(line)==0:
        break
    line=line.lstrip()
    line=line.rstrip()
    temp=line.split()
    company.append(temp)

del company[0]
file.close()

k=1
#태그를 상수로 정의함
tag_inputbox='#__next > div.SearchBar_article__XF6AA > div > div > div > div > input.SearchBar_input__t2ws8'
elem_name1='#content > div > ul > li:nth-child('+str(k)+') > div.SearchList_link__zBlL1 > strong'
elem_code1='#content > div > ul > li:nth-child('+str(k)+') > div.SearchList_link__zBlL1 > span > span.SearchList_code__59hG9'
elem_market1='#content > div > ul > li:nth-child('+str(k)+') > div.SearchList_link__zBlL1 > span > span.SearchList_market__ASMay'
#검색 결과가 하나밖에 없을 경우
elem_name2='#content > div.SearchList_article__v7J3E > ul > li > div.SearchList_link__zBlL1 > strong'
elem_code2='#content > div.SearchList_article__v7J3E > ul > li > div.SearchList_link__zBlL1 > span > span.SearchList_code__59hG9'
elem_market2='#content > div.SearchList_article__v7J3E > ul > li > div.SearchList_link__zBlL1 > span > span.SearchList_market__ASMay'
tab_statement='#_main_stock_tab > div > ul > li:nth-child(5) > a > span'
primary_statement='#content > div.RoundTab_article__lsTJ-.RoundTab_article15__vs3LK > ul > li:nth-child(2) > a'
base_day='#content > div.TableFixed_article__1mw8w > div.TableFixed_tableFrame__1Oq4s.TableFixed_scrollFrame__1gp5j > div > table > thead > tr > th:nth-last-child(1)'
btn_quater='#content > div.TabBox_tabBoxArea__38DE7.TabBox_financeTabBoxArea__Zigz- > ul > li:nth-child(2) > a'
##################### 크롤링 시작 #####################
driver = webdriver.Chrome('c:\chromedriver.exe')

url='https://m.stock.naver.com/search'
for i in range(2000,len(company)):
    print(i)    
    name=''
    code=''
    market=''
    k=1
    
    try:
        driver.get(url)
        time.sleep(0.5)
        inputbox=driver.find_element(By.CSS_SELECTOR, tag_inputbox)
        inputbox.send_keys(company[i][0].split('.')[0]) #ric를 떼어냄
        ric=company[i][0].split('.')[1]
        inputbox.send_keys(Keys.RETURN)
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
                        if check_market(ric, market): #ric에 맞는 거래소 종목을 찾는다.
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
        time.sleep(1)
        tab_statement=find_tab_statement(driver)    #child를 돌면서 재무인 것을 찾아서 확인하도록 만듦. 지렸다.
        if tab_statement=='':
            raise NoStatementException
        if is_element_present(driver, By.CSS_SELECTOR,tab_statement):
            driver.find_element(By.CSS_SELECTOR,tab_statement).click()
            time.sleep(0.3)
            if driver.find_element(By.CSS_SELECTOR,primary_statement).text=='주요재무':
                driver.find_element(By.CSS_SELECTOR,primary_statement).click()
                time.sleep(0.2)
                driver.find_element(By.CSS_SELECTOR,btn_quater).click()
                time.sleep(0.2)
                base=driver.find_element(By.CSS_SELECTOR,base_day).text
                base=base.replace('.','')
                if base!=company[i][1]:
                    output.append((i, name, company[i][0], market, company[i][1], base))
                    print('날짜가 다릅니다')
                else:
                    normal.append((i, name, company[i][0], market, company[i][1], base))
                time.sleep(0.2)
        else :
            raise NoStatementException

        

    except FindKoreaException as e:
        code=company[i][0]
        korea.append((i, code, name,market))
        print("korea : "+str(i)+' '+company[i][0]+' '+name)
        print(e)

    except TimeoutException as e:
        code=company[i][0]
        code_err=traceback.format_exc()
        no=re.search(r'line (\d+)',code_err)
        error.append((i,code, name, market,'Timeout'))
        print(str(i)+'에서 오류발생 , '+no.group()+' :')
        print(str(e))

    except NoStatementException as e:
        code=company[i][0]
        output.append((i,code, name, market,company[i][1],'No_Fin'))
        print(code+' 는 재무버튼이 없습니다.')

    except Exception as e:   #에러목록 수집
        code=company[i][0]
        code_err=traceback.format_exc()
        no=re.search(r'line (\d+)',code_err)
        error.append((i,code, name, market,'unknown error'))
        print(no.group()+' 에서 에러발생함. 일반 에러출력')
        

with open('korea.csv','a',newline='') as f:
    f.write('i,코드,상품명,거래소')
    f.write('\r\n')
    for i in korea :
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

with open('output.csv','a',newline='') as f:
    f.write('i,이름, 코드, 거래소, koscom_day, naver_day')
    f.write('\r\n')
    for i in output :
        line=''
        line=str(i[0])+','+i[1]+','+i[2]+','+i[3]+','+i[4]+','+i[5]
        f.write(line)
        f.write('\r\n')        

with open('normal.csv','a',newline='') as f:
    f.write('i,이름, 코드, 거래소, koscom_day, naver_day')
    f.write('\r\n')
    for i in normal :
        line=''
        line=str(i[0])+','+i[1]+','+i[2]+','+i[3]+','+i[4]+','+i[5]
        f.write(line)
        f.write('\r\n')        
