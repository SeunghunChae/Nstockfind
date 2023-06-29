
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

    for i in range(1,6):
        try :
            target=code1+str(i)+code2
            print(target)
            elements=driver.find_element(By.CSS_SELECTOR, target).text
            print(target)
            if elements=='재무':
                return target
        except :
            pass    
    print('재무항목이 없습니다.')
    return False

def check_market(ric, market):
    if ric=='SZ':
        if market.find('선강퉁')!=-1:
            return True
    elif ric=='SS':
        if market.find('후강퉁')!=-1:
            return True
    return False

def set_elem(k):
    global elem_name1
    global elem_code1
    global elem_market1

    elem_name1='#content > div > ul > li:nth-child('+str(k)+') > div.SearchList_link__zBlL1 > strong'
    elem_code1='#content > div > ul > li:nth-child('+str(k)+') > div.SearchList_link__zBlL1 > span > span.SearchList_code__59hG9'
    elem_market1='#content > div > ul > li:nth-child('+str(k)+') > div.SearchList_link__zBlL1 > span > span.SearchList_market__ASMay'
    return

class FindKoreaException(Exception): ## Exception을 상속받아야한다.
    def __init__(self):
        super().__init__('한국종목이 나왔습니다.') 

class TimeoutException(Exception): ## while이 3초 이상 돌 경우
    def __init__(self,timeout):
        super().__init__(f"while이 {timeout} 초 이상 돌았습니다.")

class NoStatementException(Exception): ## while이 3초 이상 돌 경우
    def __init__(self):
        super().__init__(f"재무버튼이 없습니다.")
