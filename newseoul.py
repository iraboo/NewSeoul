import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
import bookingAPI
from MyLogger import get_logger

#############################################################################
# 뉴서울
#
# 1개월전 오전 10시
# 로그인 ID/PASSWORD, 예약을 원하는 월, 일, 시간, 시간대 입력

# 예약에 필요한 정보를 입력
ID = '0739'
PASSWD = 'shin00^^'
MONTH = '2023 / 03'         # 포맷 = 'yyyy / mm' (ex) '2022 / 06'
DATE = '23'                  # 포맷 = 'd' (ex) '8', '29'
TIMEZONE = '07'             # 포맷 = 'hh' (ex) '07' '12'
#ORDER = 15                 # 예약시간대에서 몇번째 예약시간을 예약할지를 입력, 0 첫번째
START = '100001'            # 부킹시작 시간
DEBUG = 1                   # if TEST, DEBUG = 1
#############################################################################

logger = get_logger('newseoul')
booking = bookingAPI.GolfBooking()

# 웹사이트 접속
url = 'https://www.newseoulgolf.co.kr/join/login.asp'
booking.browser.get(url)

# ID, Password 입력하고 LOGIN 버튼
booking.browser.find_element(By.XPATH, '//*[@id="txtId"]').send_keys(ID)
booking.browser.find_element(By.XPATH, '//*[@id="txtPw"]').send_keys(PASSWD)
booking.browser.find_element(By.XPATH, '//*[@id="contents"]/div/div[2]/form/div[2]/div/a').click()

# 화면상단 퀵메뉴의 실시간예약 버튼
booking.browser.find_element(By.XPATH, '//*[@id="mainMenu"]/div[1]/a[1]').send_keys('\n') 

# 실시간예약 화면에서 월 선택
monthlist = booking.browser.find_element(By.CLASS_NAME, 'monthChoice').find_element(By.TAG_NAME, 'p')
if monthlist.text == MONTH:
    month_id = 'calendarBox1' 
else:
    month_id = 'calendarBox2'
logger.info('예약월 = %s', MONTH)  

if DEBUG:   # For TEST
    datelist = booking.browser.find_element(By.ID, month_id).\
        find_element(By.TAG_NAME, 'tbody').find_elements(By.CLASS_NAME, 'possible')
else:    
# 예약시작 10분전에 로그인하고 실시간예약화면에서 대기
# 예약시간(START)이 되면 화면을 refresh하고 예약할 날짜를 선택
    while True:     
        if(time.strftime('%H%M%S') == START):
            booking.browser.refresh() 
            datelist = booking.browser.find_element(By.ID, month_id). \
                find_element(By.TAG_NAME, 'tbody').find_elements(By.CLASS_NAME, 'possible')
            break
        time.sleep(1)   # while문 1초씩 증가

for t in datelist:
    a = t.text.split()
    if a[0] == DATE:
        logger.info('예약일 = %s', DATE)
        t.click()
        break

# course 리스트에 있는 순서대로 코스별 예약가능한 시간을 가져와서
# 원하는 시간대(TIMEZONE)에 예약을 진행   
# Ex) course = [예술OUT, 예술IN, 문화OUT, 문화IN] = [y_out, y_in, m_out, m_in]
y_out = 'cosAContainer'; y_in = 'cosBContainer'     # 예술코스
m_out = 'cosCContainer'; m_in = 'cosDContainer'     # 문화코스
course = [m_out, m_in, y_out, y_in]
breaker = 0
for t in course:
    timelist = booking.browser.find_element(By.ID, t).find_elements(By.TAG_NAME, 'li')
    for k in timelist:
        if k.text[:2] == TIMEZONE:
            logger.info('Java Script = %s', k.get_attribute('onclick'))
            booking.browser.execute_script(k.get_attribute('onclick'))
            breaker = 1
            break
    if breaker == 1:
        break
time.sleep(1)    
   
try:
    #Alert(booking.browser).accept()     # 예약 확인    
    Alert(booking.browser).dismiss()    # 예약 취소
except:
    logger.info('%s시 시간대 예약이 가능하지 않습니다', TIMEZONE)
else:
    logger.info('%s시 시간대에 예약되었습니다', TIMEZONE)

time.sleep(1)

'''
if breaker == 0:
    logger.info('%s시 시간대 예약이 가능하지 않습니다', TIMEZONE)
else:
    # 예약 컨펌 팝업창
    #Alert(booking.browser).accept()     # 예약 확인    
    Alert(booking.browser).dismiss()    # 예약 취소
''' 

# 텔레그램 전송기능 구현

