from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoAlertPresentException,
    UnexpectedAlertPresentException,
    TimeoutException
)
import pickle
import time

def get_login_eta(selected_board, title, content, extra_files, hash_code):
    driver = webdriver.Chrome()
    driver.get("https://everytime.kr")  # 쿠키 적용할 사이트 먼저 접속

    # 쿠키 로드
    with open("et_cookies.pkl", "rb") as f:
        cookies = pickle.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)
    # 새로고침하면 로그인된 상태로 전환됨
    driver.refresh()
    time.sleep(3)
    print("✅ 자동 로그인 성공")

    board_menu = driver.find_element(By.LINK_TEXT, "게시판")
    board_menu.click()
    print("✅ 게시판 클릭 성공")
    board_map = {
        "동아리·학회": "/418774",
        "홍보게시판": "/367436",
        "자유게시판": "/377387",
        "새내기게시판": "/385882",
        "정보게시판": "/258609"
    }
    print(f"selected_board : {selected_board}")
    for board in selected_board:
        print("✔ 선택된 게시판:", board)
        if board in board_map:
            url = "https://everytime.kr" + board_map[board]
            print("게시판 URL:", url)
            driver.get(url)
            wait = WebDriverWait(driver, 10)
            write_btn = wait.until(EC.element_to_be_clickable((By.ID, "writeArticleButton")))
            write_btn.click()

            time.sleep(2)
            # 제목 입력
            title_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='title'].title")))
            title_input.clear()
            title_input.send_keys(title)
            # 내용
            text_area = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "text"))
            )

            # 텍스트 입력
            text_area.clear()
            driver.execute_script("""
                arguments[0].value = arguments[1];
                arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            """, text_area, content)
            time.sleep(2)
            
            # 해시태그
            text_area.send_keys(hash_code)
            # 첨부 파일
            upload_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file'].file")))

            # 여러 파일을 동시에 넘기기 (경로는 절대 경로여야 함)
            upload_input.send_keys("\n".join(extra_files))
            time.sleep(3)
            # 익명 버튼 무조건 클릭
            anon_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "anonym"))
            )
            anon_button.click()
            # 제출 버튼
            time.sleep(2)
            submit_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "ul.option li.submit")))
            submit_btn.click()
            # 확인 버튼이 나타날 때까지 대기 후 클릭
            
            try:
                WebDriverWait(driver, 5).until(EC.alert_is_present())  # 5초간 alert 대기
                alert = driver.switch_to.alert
                print("⚠️ Alert 팝업 내용:", alert.text)
                alert.accept()
                print("✅ Alert 확인 클릭 완료")
                time.sleep(3)
                continue

            except TimeoutException:
                print("⏱️ Timeout: alert이 감지되지 않음. 다음으로 진행.")

            except NoAlertPresentException:
                print("ℹ️ NoAlertPresentException: alert 없음")

            except UnexpectedAlertPresentException:
                try:
                    alert = driver.switch_to.alert
                    print("⚠️ Unexpected Alert:", alert.text)
                    alert.accept()
                    print("✅ 강제 Alert 확인 완료")
                except Exception as e:
                    print("❌ Alert 처리 중 오류:", e)

            # 다음 게시판 처리를 위해 잠시 대기
            time.sleep(3)
        else:
            print(f"⚠ 알 수 없는 게시판: {board}")
if __name__ == "__main__":
    get_login_eta()



    