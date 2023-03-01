import time, sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
import config

class GolfBooking():
    def __init__(self):
        current_folder = config.PROJECT_DIR
        chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]  #크롬드라이버 버전 확인
        chrome_file = current_folder + chrome_ver + '/chromedriver'
        
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])    
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        #options.add_argument('headless')    # 크롬을 백그라운드에서 실행
        options.add_argument( "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")     # 봇으로 인식하지 않게끔 설정
        ser = Service(chrome_file)
        
        try:
            self.browser = webdriver.Chrome(service=ser, options=options)
        except:     # 크롬버전이 다르면 ./{chrome_ver}에 다시 설치
            chromedriver_autoinstaller.install(True)
            self.browser = webdriver.Chrome(service=ser, options=options)
            
        self.browser.implicitly_wait(10) # seconds
        
        
    # 로그인화면에 접속, ID/PASSWD 입력, 실시간예약 버튼을 누른다
    # url: 로그인 화면
    # username = ID, passwd = PASSWD
    # login_xpath: ['ID input xpath', 'PASSWD input xpath', 'login button xpath']  
    #              [ID 입력창, 패스워드 입력창, 로그인 버튼, 실시간예약 버튼]  
    def login_by_xpath(self, url, username, passwd, login_xpath):
        self.browser.get(url)
        self.browser.find_element(By.XPATH, login_xpath[0]).send_keys(username)
        self.browser.find_element(By.XPATH, login_xpath[1]).send_keys(passwd)
        self.browser.find_element(By.XPATH, login_xpath[2]).click()     
            
        
    # 실시간예약 버튼
    # xpath = 실시간예약 버튼 xpath
    def button_by_xpath(self, xpath):    
        booking_bt = self.browser.find_element(By.XPATH, xpath)
        booking_bt.send_keys('\n') 
        
        
    # 로그인/예약 컨펌 팝업창
    def confirm(self, ok):      
        if ok == 1:
            alert = Alert(self.browser)
            alert.accept()      # 예약 확인
        else:
            alert.dismiss()     # 예약 취소
        
        
    # 예약내용 확인하고 OK/CANCEL
    def w_confirm(self, ok):
        if ok == 1:     # 예약 OK
            confirm = self.browser.find_element(By.ID, 'DOMWindow'). \
                find_element(By.CLASS_NAME, 'cm_ok').find_element(By.TAG_NAME,'a')
            confirm.send_keys('\n')      # 예약 확인
        else:           # 예약내용 취소, cm_calcle 스펠링 주의!!!
            cancel = self.find_element(By.ID, 'DOMWindow'). \
                find_element(By.CLASS_NAME, 'cm_cancle').find_element(By.TAG_NAME,'a')
            cancel.send_keys('\n')   