from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
import time
import getpass

print('============================ 고성CC 예약 매크로 ================================')
print('1. 해상도 1920 X 1080 기준으로 개발되었음')
print('2. 입력한 날짜가 예약 불가(오픈 전/마감)일 경우')
print('   → 새로고침 반복 (현재 무한 반복) 중 예약 가능으로 바뀌면 진행')
print('3. 입력한 시간대 중 가장 빠른 시간으로 예약')
print('4. 입력한 시간대 중 예약 가능한 시간이 없는 경우')
print('   → 새로고침 반복 (현재 무한 반복) 중 예약 가능 시간이 생기면 진행')
print('5. 예매 완료 시 자동 종료됨')
print('6. 다른 사용자와 예매 타이밍이 겹치는 경우에 대해서는 미처리')
print('================================================================================')
print('!주의! 입력값에 대한 검증은 되어있지 않으니 반드시 다음 규칙에 따라 입력하세요')
print('!주의! 공백 포함될 경우 해당 부분에서 무한 반복')
print('1. 아이디 비밀번호 일치여부는 매크로에서 확인 불가하므로 정확하게 입력하세요')
print('2. 비밀번호 입력 시 입력 값이 노출되지 않습니다')
print('3. 예약일은 8자리 숫자로만 입력해주세요 (예) 20220408')
print('4. 예약시간대는 2자리 숫자로만 입력해주세요 (예) 07 18')
print('5. 예약인원은 숫자 3 또는 4 한자리만 입력해주세요 (예) 4')
print('================================================================================')

# 사용자입력받기
userID = input('아이디 : ')
userPW = getpass.getpass('비밀번호 : ')
userDate = input('예약일 (8자리) : ')
userTime = input('예약시간대 (2자리) : ')
userPerson = input('예약인원 (3,4) : ')

# 간격 설정(초)
timeRefresh = 10 # 새로고침
timeLoading = 60 # 페이지로딩

# 드라이버 연결
path = "C:\\Python\\chromedriver.exe"
driver = webdriver.Chrome(path);

# 크롬 오픈
driver.get("http://www.gosungcc.com/07member/login.asp")
driver.maximize_window()
driver.implicitly_wait(timeLoading)

# 로그인
driver.find_element(By.XPATH, '//*[@id="wrap"]/div[2]/div[2]/div[2]/div/ul/li[4]/ul/form/li/ul/li[2]/input').send_keys(userID)
driver.find_element(By.XPATH, '//*[@id="wrap"]/div[2]/div[2]/div[2]/div/ul/li[4]/ul/form/li/ul/li[5]/input').send_keys(userPW) 
driver.find_element(By.XPATH, '//*[@id="wrap"]/div[2]/div[2]/div[2]/div/ul/li[4]/ul/form/li/div/a').click()
driver.implicitly_wait(timeLoading)

# 팝업 닫기
tabs = driver.window_handles
nTabs = len(tabs)
while nTabs > 1 :
    driver.switch_to.window(tabs[nTabs-1]) # 맨 뒤부터 제거
    driver.close()
    nTabs -= 1
driver.switch_to.window(tabs[0]) # 메인

# 예약 페이지 이동
driver.get('http://www.gosungcc.com/05reservation/01reservation.asp')
driver.implicitly_wait(timeLoading)

# 날짜 선택
bDate = userDate 
bDateScript = 'javascript:transDate('+bDate+')' # 예약하고 싶은 날짜 선택 스크립트
bPossible = False # 초기화
while True : # 예약 불가일 경우 루프
    book = driver.find_elements(By.CLASS_NAME, 'possible') # 예약 가능 
    for pBook in book :
        pBookClick = pBook.get_attribute("onclick") # onclick 추출
        if pBookClick.find(bDate) != -1 : # 예약 가능
            bPossible = True 
            break
    if bPossible == True : break # 예약가능할 경우 종료
    # 예약불가할 경우 새로고침
    time.sleep(timeRefresh)
    driver.refresh() 
# 날짜 스크립트 실행
driver.execute_script(bDateScript)
driver.implicitly_wait(timeLoading)

# 시간 선택
bTime = userTime
bTimeSearch = bTime + ' :' # 시간으로 검색, 분단위에 포함가능성 있어서 : 붙임
tPossible = False; # 초기화
tIndex = 2 # 초기화
while True : 
    tOk = driver.find_elements(By.CLASS_NAME, 'reserOk') # 예약 가능한 시간대 가져오기
    tIndex = 2 # 초기화
    for i in tOk: # 예약하고 싶은 시간대 찾기
        if i.text.find(bTimeSearch) != -1 : 
            tPossible = True; # 예약하고 싶은 시간대 있음
            break # 반복 종료
        tIndex += 1 # 없는 경우 인덱스번호 증가
    if tPossible == True : break # 예약 가능할 경우 루프 종료
    # 예약하고 싶은 시간대 없는 경우 새로고침
    time.sleep(timeRefresh) 
    driver.refresh() 

# 인원 선택
nPerson = int(userPerson)
driver.find_element(By.XPATH, '//*[@id="wrap"]/div[2]/div[2]/div[2]/div[2]/table/tbody/tr['+str(tIndex)+']/td[2]/input['+str(nPerson-2)+']').click()

# 예약하기 클릭
driver.find_element(By.XPATH, '//*[@id="wrap"]/div[2]/div[2]/div[2]/div[2]/table/tbody/tr['+str(tIndex)+']/td[4]/a/span').click()
driver.implicitly_wait(timeLoading)

# 예약하기 클릭
driver.find_element(By.XPATH, '//*[@id="wrap"]/div[2]/div[2]/div[2]/div[3]/ul/li[1]/a').click()

# 팝업창 예약 클릭
reserYes = Alert(driver)
reserYes.accept()
# 팝업창 확인 클릭
reserOk = Alert(driver)
reserOk.accept()

# 종료
time.sleep(timeRefresh)
driver.quit()
