import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@pytest.fixture
def driver():
    d = webdriver.Chrome()
    d.maximize_window()
    yield d
    d.quit()

# ————————————————————————————————
# TEST 1: Login Berhasil (Contoh: akun admin)
# ————————————————————————————————
def test_login_success(driver):
    driver.get("http://localhost/project_april/login.php")
    wait = WebDriverWait(driver, 10)

    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("123")
    driver.find_element(By.XPATH, "//button[@type='submit' or @value='Login']").click()

    wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
    
    driver.save_screenshot("test1_login_berhasil.png")
    assert "Dashboard" in driver.title or "Welcome, Admin" in driver.page_source

# ————————————————————————————————
# TEST 2: Login Gagal – Password Salah
# ————————————————————————————————
def test_login_password_salah(driver):
    driver.get("http://localhost/project_april/login.php")

    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("password123")
    driver.find_element(By.XPATH, "//button[@type='submit' or @value='Login']").click()

    try:
        error_elem = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-danger"))
        )
    except:
        
        error_elem = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'salah') or contains(text(), 'gagal') or contains(text(), 'error')]"))
        )

    driver.save_screenshot("test2_password_salah.png")
    assert error_elem.is_displayed()

# ————————————————————————————————
# TEST 3: Login dengan Field Kosong
# ————————————————————————————————
def test_login_kosong(driver):
    driver.get("http://localhost/project_april/login.php")

    
    driver.find_element(By.XPATH, "//button[@type='submit' or @value='Login']").click()

    time.sleep(2)
    driver.save_screenshot("test3_form_kosong.png")

    assert "login" in driver.current_url.lower()