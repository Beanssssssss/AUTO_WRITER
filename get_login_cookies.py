from selenium import webdriver
import pickle
import time

driver = webdriver.Chrome()
driver.get("https://everytime.kr/login")

# 수동 or 자동 로그인
time.sleep(30)  # 수동 로그인 시간 줌 이 시간 동안 로그인 하면 됌

# 로그인 완료되면 쿠키 저장
with open("et_cookies.pkl", "wb") as f:
    pickle.dump(driver.get_cookies(), f)

print("✅ 쿠키 저장 완료")
driver.quit()