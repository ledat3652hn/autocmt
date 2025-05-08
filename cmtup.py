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

# ❌ KHÔNG dùng đường dẫn Windows nữa
# service = Service(r"E:\chromedriver-win64\chromedriver-win64\chromedriver.exe")

# ✅ Dùng mặc định, ChromeDriver đã được cài sẵn trong workflow
driver = webdriver.Chrome(options=options)

# ================== ĐĂNG NHẬP BẰNG COOKIE ==================
print("🔐 Đang mở Facebook và chờ tải trang...")
driver.get("https://www.facebook.com/")
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

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

if "login" in driver.current_url or "recover" in driver.current_url:
    print("❌ Cookie đã hết hạn hoặc sai! Không đăng nhập được.")
    driver.quit()
    exit()
else:
    print("✅ Cookie hợp lệ, đã đăng nhập thành công vào Facebook!")

# ================== CÁC HÀM CŨ GIỮ NGUYÊN ==================
# Giữ nguyên toàn bộ phần comment_and_delete() và xử lý phía sau

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
