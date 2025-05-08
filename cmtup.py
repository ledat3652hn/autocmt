from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ================== CẤU HÌNH DRIVER ==================
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--log-level=3")
options.add_argument("--disable-extensions")
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)

service = Service(r"E:\chromedriver-win64\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

# ================== ĐĂNG NHẬP BẰNG COOKIE ==================
print("🔐 Đang mở Facebook và chờ tải trang...")
driver.get("https://www.facebook.com/")
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

#COOKIES dạng list dictionary
cookies = [
    {'name': 'c_user', 'value': '100005668125883'},
    {'name': 'datr', 'value': 'f874Z8BHYmHXOmaO2NUg1N_a'},
    {'name': 'fr', 'value': '1YGo8LGEsK7v5yRwf.AWf02Eq7Atdzkb1SpOZQYsDuwXPN6b4F-TRxul7udW-WGc3hROs.BoEF3H..AAA.0.0.BoEF3H.AWcaAyDJrDatYaqNC4qtsdLWuxs'},
    {'name': 'locale', 'value': 'vi_VN'},
    {'name': 'presence', 'value': 'C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1745904982420%2C%22v%22%3A1%7D'},
    {'name': 'ps_l', 'value': '1'},
    {'name': 'ps_n', 'value': '1'},
    {'name': 'sb', 'value': 'f874Z7UmICxcnVpDx3yV4wdM'},
    {'name': 'wd', 'value': '1875x919'},
    {'name': 'xs', 'value': '4%3A32YQpDeZ2vS4aw%3A2%3A1745893754%3A-1%3A7477%3A%3AAcUuP3Kcy-JniOKmWq5DcQmVxk_SN_2aAismcqGt3g'}
]

print("🍪 Đang thêm cookie đăng nhập...")
for cookie in cookies:
    driver.add_cookie(cookie)

driver.refresh()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
time.sleep(2)

# ================== KIỂM TRA ĐĂNG NHẬP THẬT ==================
if "login" in driver.current_url or "recover" in driver.current_url:
    print("❌ Cookie đã hết hạn hoặc sai! Không đăng nhập được.")
    driver.quit()
    exit()
else:
    print("✅ Cookie hợp lệ, đã đăng nhập thành công vào Facebook!")

# ================== FUNCTION COMMENT & DELETE ==================
def comment_and_delete(post_id):
    driver.get(f"https://www.facebook.com/{post_id}")
    time.sleep(3)

    comment_text = "Up"
    wait = WebDriverWait(driver, 10)

    # ================== COMMENT ==================
    try:
        comment_box = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@aria-label='Viết bình luận...' or contains(@aria-label, 'bình luận')][@role='textbox']"))
        )
        actions = ActionChains(driver)
        actions.move_to_element(comment_box).click().perform()
        time.sleep(0.5)

        comment_box.send_keys(comment_text)
        time.sleep(0.5)
        comment_box.send_keys(Keys.ENTER)
        print(f"✅ Đã comment thành công bài {post_id}: {comment_text}")

        time.sleep(5)

    except Exception as e:
        print(f"❌ Lỗi comment bài {post_id}: {e}")
        return

    # ================== TÌM COMMENT VỚI RETRY ==================
    def find_my_comment_with_retry(driver, text_comment, max_retry=5, delay=2):
        for attempt in range(max_retry):
            comment_block = find_my_comment(driver, text_comment)
            if comment_block:
                return comment_block
            print(f"⏳ Không tìm thấy comment lần {attempt+1}, chờ {delay}s rồi thử lại...")
            time.sleep(delay)
        return None

    def find_my_comment(driver, text_comment, timeout=10):
        wait = WebDriverWait(driver, timeout)
        try:
            wait.until(EC.presence_of_element_located(
                (By.XPATH, '//div[contains(@aria-label, "Bình luận") or contains(@aria-label, "Comment")]')))
            comment_blocks = driver.find_elements(By.XPATH,
                '//div[contains(@aria-label, "Bình luận") or contains(@aria-label, "Comment")]')

            for block in reversed(comment_blocks):
                try:
                    text_element = block.find_element(By.XPATH, './/div/div/div/span/div/div')
                    if text_comment.strip() == text_element.text.strip():
                        print(f"✅ Tìm thấy comment bài {post_id}: {text_element.text.strip()}")
                        return block
                except Exception:
                    continue
            return None

        except Exception as e:
            print(f"❌ Lỗi tìm comment bài {post_id}: {e}")
            return None

    def delete_comment(comment_block):
        try:
            actions = ActionChains(driver)
            actions.move_to_element(comment_block).perform()
            time.sleep(0.5)

            more_button = comment_block.find_element(By.XPATH, ".//div[@role='button' and @aria-haspopup='menu']")
            more_button.click()
            print(f"✅ Đã bấm 3 chấm bài {post_id}!")

            delete_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//span[text()="Xóa"]'))
            )
            delete_button.click()
            print(f"✅ Đã click nút Xóa bài {post_id}!")

            confirm_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//span[text()="Xóa"]/ancestor::div[@role="button"]'))
            )
            confirm_button.click()
            print(f"✅ Đã xác nhận xóa comment bài {post_id}!")

        except Exception as e:
            print(f"❌ Lỗi khi thực hiện thao tác xóa comment bài {post_id}: {e}")

    # ================== QUY TRÌNH XÓA ==================
    comment_block = find_my_comment_with_retry(driver, comment_text)

    if comment_block:
        delete_comment(comment_block)
        time.sleep(5)

        # Kiểm tra comment đã bị xóa chưa
        try:
            WebDriverWait(driver, 5).until_not(
                EC.presence_of_element_located((By.XPATH, f"//span[text()='{comment_text}']"))
            )
            print(f"✅ Comment đã biến mất bài {post_id} sau lần xóa đầu tiên!")
        except:
            print(f"⚠️ Comment vẫn còn sau lần xóa đầu tiên bài {post_id}, thử xóa lần 2...")

            # Thử xóa lần nữa
            comment_block_retry = find_my_comment_with_retry(driver, comment_text)
            if comment_block_retry:
                delete_comment(comment_block_retry)
                time.sleep(5)

                try:
                    WebDriverWait(driver, 5).until_not(
                        EC.presence_of_element_located((By.XPATH, f"//span[text()='{comment_text}']"))
                    )
                    print(f"✅ Comment đã biến mất bài {post_id} sau lần xóa thứ 2!")
                except:
                    print(f"❌ Xóa 2 lần vẫn không mất comment bài {post_id}!")
            else:
                print(f"❌ Không tìm thấy comment để retry xóa bài {post_id}!")
    else:
        print(f"❌ Không tìm thấy comment để xóa bài {post_id}.")

# ================== CHẠY NHIỀU BÀI ==================
post_ids = [
    "1395462074452185",
    "1530105834321141",
    "549278304834438",
    "537519532676982",
    "1168701231445070",
    "1162808585367668",
    "990016512718211",
    "987734636279732",
    "1423927608638171",
    "2110303836004279",
    "2089017381466258",
    "1735826397013278",
    "1337486793948920",
    "1211360109894923",
    "1421752431823149"
]

for pid in post_ids:
    comment_and_delete(pid)

driver.quit()



