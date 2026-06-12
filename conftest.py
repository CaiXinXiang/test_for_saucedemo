import glob as _glob
import os as _os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def _find_chromedriver():
    """在 webdriver-manager 缓存中查找 ChromeDriver，避免每次加锁"""
    wdm_dir = _os.path.join(_os.path.expanduser("~"), ".wdm", "drivers", "chromedriver", "win64")
    if _os.path.isdir(wdm_dir):
        drivers = _glob.glob(_os.path.join(wdm_dir, "*", "chromedriver-win64", "chromedriver.exe"))
        if drivers:
            return max(drivers, key=_os.path.getmtime)
    raise FileNotFoundError("ChromeDriver 未找到，请先运行一次 webdriver-manager 下载")


_CHROMEDRIVER_PATH = _find_chromedriver()


@pytest.fixture(scope="function")
def driver():
    """初始化 Chrome WebDriver，每个测试用例结束后关闭"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    service = Service(_CHROMEDRIVER_PATH)
    drv = webdriver.Chrome(service=service, options=options)
    drv.implicitly_wait(5)
    yield drv
    drv.quit()


@pytest.fixture(scope="function")
def logged_in_driver(driver):
    """已登录状态的 driver，跳过登录步骤直接进入商品页"""
    driver.get("https://www.saucedemo.com/")
    from pages.login_page import LoginPage
    login_page = LoginPage(driver)
    login_page.login("standard_user", "secret_sauce")
    return driver
