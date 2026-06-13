"""
SauceDemo 自动化测试脚本
======================
覆盖：登录、商品浏览、购物车、结账全流程
技术栈：Python + Selenium + Pytest + Page Object
学习用途：软件测试工程师练手项目

使用前请安装依赖：
    pip install selenium webdriver-manager pytest

运行方法：
    pytest test_saucedemo.py -v --html=report.html
"""

import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


# ============================================================
# 配置区：所有账号信息
# ============================================================
BASE_URL = "https://www.saucedemo.com"
PASSWORD = "secret_sauce"

USERS = {
    "standard": "standard_user",
    "locked": "locked_out_user",
    "problem": "problem_user",
    "performance": "performance_glitch_user",
    "error": "error_user",
    "visual": "visual_user",
}


# ============================================================
# 工具函数
# ============================================================

def get_driver():
    """初始化 Chrome 浏览器驱动"""
    options = Options()
    options.add_argument("--window-size=1280,720")
    # 取消下面注释可以无头模式运行（不弹出浏览器窗口）
    # options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)
    return driver


# ============================================================
# 测试用例 1：登录功能测试
# ============================================================

class TestLogin:
    """
    覆盖场景：
    1. 正常用户成功登录
    2. 锁定用户登录被拒
    3. 空用户名
    4. 空密码
    5. 错误密码
    """

    def setup_method(self):
        self.driver = get_driver()
        self.driver.get(BASE_URL)

    def teardown_method(self):
        self.driver.quit()

    def test_login_success_standard_user(self):
        """TC-001：standard_user 正常登录"""
        self.driver.find_element(By.ID, "user-name").send_keys(USERS["standard"])
        self.driver.find_element(By.ID, "password").send_keys(PASSWORD)
        self.driver.find_element(By.ID, "login-button").click()
        # 验证：跳转到商品列表页
        assert self.driver.current_url == f"{BASE_URL}/inventory.html", "登录后应该跳转到商品列表页"
        print("[PASS] standard_user 登录成功")

    def test_login_locked_out_user(self):
        """TC-002：locked_out_user 登录被拒"""
        self.driver.find_element(By.ID, "user-name").send_keys(USERS["locked"])
        self.driver.find_element(By.ID, "password").send_keys(PASSWORD)
        self.driver.find_element(By.ID, "login-button").click()
        # 验证：显示锁定错误提示
        error_msg = self.driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
        assert "locked out" in error_msg.text.lower(), "应该显示锁定提示"
        print(f"[PASS] locked_out_user 登录被拒，错误信息: {error_msg.text}")

    def test_login_empty_username(self):
        """TC-003：用户名为空"""
        self.driver.find_element(By.ID, "password").send_keys(PASSWORD)
        self.driver.find_element(By.ID, "login-button").click()
        error_msg = self.driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
        assert "Username is required" in error_msg.text
        print(f"[PASS] 空用户名提示正确: {error_msg.text}")

    def test_login_empty_password(self):
        """TC-004：密码为空"""
        self.driver.find_element(By.ID, "user-name").send_keys(USERS["standard"])
        self.driver.find_element(By.ID, "login-button").click()
        error_msg = self.driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
        assert "Password is required" in error_msg.text
        print(f"[PASS] 空密码提示正确: {error_msg.text}")

    def test_login_wrong_password(self):
        """TC-005：密码错误"""
        self.driver.find_element(By.ID, "user-name").send_keys(USERS["standard"])
        self.driver.find_element(By.ID, "password").send_keys("wrong_password")
        self.driver.find_element(By.ID, "login-button").click()
        error_msg = self.driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
        assert "do not match" in error_msg.text
        print(f"[PASS] 密码错误提示正确: {error_msg.text}")


# ============================================================
# 测试用例 2：商品浏览与购物车功能
# ============================================================

class TestProducts:
    """
    覆盖场景：
    1. 商品列表加载正常
    2. 按名称排序
    3. 按价格排序
    4. 添加商品到购物车
    5. 移除商品
    6. 购物车角标正确显示
    """

    def setup_method(self):
        self.driver = get_driver()
        self.driver.get(BASE_URL)
        # 先登录
        self.driver.find_element(By.ID, "user-name").send_keys(USERS["standard"])
        self.driver.find_element(By.ID, "password").send_keys(PASSWORD)
        self.driver.find_element(By.ID, "login-button").click()

    def teardown_method(self):
        self.driver.quit()

    def test_product_list_displays_all_items(self):
        """TC-006：商品列表显示6件商品"""
        items = self.driver.find_elements(By.CLASS_NAME, "inventory_item")
        assert len(items) == 6, f"应该显示6件商品，实际显示{len(items)}件"
        print(f"[PASS] 商品列表共 {len(items)} 件商品")

    def test_sort_by_name_az(self):
        """TC-007：按名称 A→Z 排序"""
        sort_select = Select(self.driver.find_element(By.CLASS_NAME, "product_sort_container"))
        sort_select.select_by_value("az")
        time.sleep(0.5)
        names = self.driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        name_texts = [n.text for n in names]
        assert name_texts == sorted(name_texts), "商品应按名称 A→Z 排序"
        print(f"[PASS] A→Z 排序正确: {name_texts[0]} → {name_texts[-1]}")

    def test_sort_by_price_low_to_high(self):
        """TC-008：按价格从低到高"""
        sort_select = Select(self.driver.find_element(By.CLASS_NAME, "product_sort_container"))
        sort_select.select_by_value("lohi")
        time.sleep(0.5)
        prices = self.driver.find_elements(By.CLASS_NAME, "inventory_item_price")
        price_values = [float(p.text.replace("$", "")) for p in prices]
        assert price_values == sorted(price_values), "价格应从低到高"
        print(f"[PASS] 价格排序正确: ${price_values[0]} → ${price_values[-1]}")

    def test_add_single_item_to_cart(self):
        """TC-009：添加一件商品到购物车"""
        add_btn = self.driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
        add_btn.click()
        badge = self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        assert badge.text == "1", "购物车角标应为1"
        print(f"[PASS] 添加1件商品，购物车角标: {badge.text}")

    def test_add_multiple_items_to_cart(self):
        """TC-010：添加多件商品"""
        buttons = self.driver.find_elements(By.CSS_SELECTOR, "[class*='btn_inventory']")
        for btn in buttons[:3]:
            btn.click()
        badge = self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        assert badge.text == "3", "购物车角标应为3"
        print(f"[PASS] 添加3件商品，购物车角标: {badge.text}")

    def test_remove_item_from_cart(self):
        """TC-011：移除商品"""
        self.driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
        self.driver.find_element(By.ID, "remove-sauce-labs-backpack").click()
        with pytest.raises(NoSuchElementException):
            self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        print("[PASS] 移除后购物车角标消失")


# ============================================================
# 测试用例 3：下单流程
# ============================================================

class TestCheckout:
    """
    覆盖场景：
    1. 完整下单流程（加购→结账→填信息→完成）
    2. 名称为空校验
    3. 取消订单
    """

    def setup_method(self):
        self.driver = get_driver()
        self.driver.get(BASE_URL)
        self.driver.find_element(By.ID, "user-name").send_keys(USERS["standard"])
        self.driver.find_element(By.ID, "password").send_keys(PASSWORD)
        self.driver.find_element(By.ID, "login-button").click()
        # 先添加一件商品
        self.driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()

    def teardown_method(self):
        self.driver.quit()

    def test_complete_checkout(self):
        """TC-012：完整下单流程"""
        # 进入购物车
        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        assert self.driver.current_url.endswith("/cart.html")

        # 点击 Checkout
        self.driver.find_element(By.ID, "checkout").click()
        assert self.driver.current_url.endswith("/checkout-step-one.html")

        # 填写信息
        self.driver.find_element(By.ID, "first-name").send_keys("张三")
        self.driver.find_element(By.ID, "last-name").send_keys("测试")
        self.driver.find_element(By.ID, "postal-code").send_keys("100000")
        self.driver.find_element(By.ID, "continue").click()
        assert self.driver.current_url.endswith("/checkout-step-two.html")

        # 确认订单
        self.driver.find_element(By.ID, "finish").click()
        assert self.driver.current_url.endswith("/checkout-complete.html")

        # 验证成功信息
        complete_header = self.driver.find_element(By.CLASS_NAME, "complete-header")
        assert "Thank you" in complete_header.text
        print(f"[PASS] 下单成功: {complete_header.text}")

    def test_checkout_missing_first_name(self):
        """TC-013：结账时名称为空"""
        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        self.driver.find_element(By.ID, "checkout").click()
        # 不填名称，直接点 Continue
        self.driver.find_element(By.ID, "last-name").send_keys("测试")
        self.driver.find_element(By.ID, "postal-code").send_keys("100000")
        self.driver.find_element(By.ID, "continue").click()
        error = self.driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
        assert "First Name is required" in error.text
        print(f"[PASS] 名称校验正确: {error.text}")

    def test_cancel_checkout(self):
        """TC-014：取消结账"""
        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        self.driver.find_element(By.ID, "checkout").click()
        self.driver.find_element(By.ID, "cancel").click()
        assert self.driver.current_url.endswith("/cart.html"), "取消后应返回购物车"
        print("[PASS] 取消结账，正确返回购物车")


# ============================================================
# 测试用例 4：不同账号的异常行为对比
# ============================================================

class TestDifferentUsers:
    """
    覆盖场景：对比不同账号的行为差异
    特别注意 problem_user 和 error_user 的异常行为
    """

    def test_problem_user_image_broken(self):
        """TC-015：problem_user 图片加载异常"""
        driver = get_driver()
        driver.get(BASE_URL)
        driver.find_element(By.ID, "user-name").send_keys(USERS["problem"])
        driver.find_element(By.ID, "password").send_keys(PASSWORD)
        driver.find_element(By.ID, "login-button").click()
        time.sleep(1)

        # 检查商品图片
        images = driver.find_elements(By.CSS_SELECTOR, ".inventory_item_img img")
        broken_images = 0
        for img in images:
            src = img.get_attribute("src")
            if "sl-404" in src or "WithGarbageOnImgToFeel" in src:
                broken_images += 1
                print(f"  [BUG] 异常图片: {src}")

        print(f"[INFO] problem_user 异常图片数: {broken_images}/6")
        driver.quit()

    def test_performance_user_slow_load(self):
        """TC-016：performance_glitch_user 加载缓慢（测超时处理）"""
        driver = get_driver()
        driver.get(BASE_URL)

        start_time = time.time()
        driver.find_element(By.ID, "user-name").send_keys(USERS["performance"])
        driver.find_element(By.ID, "password").send_keys(PASSWORD)
        driver.find_element(By.ID, "login-button").click()

        # 等待商品列表加载（需要更长的等待时间）
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
            )
            load_time = time.time() - start_time
            print(f"[INFO] performance_user 登录耗时: {load_time:.2f}秒")
            assert load_time > 2, "该用户应该有明显的加载延迟"
        except TimeoutException:
            print("[FAIL] performance_user 加载超时！")

        driver.quit()

    def test_error_user_add_to_cart_issues(self):
        """TC-017：error_user 加购操作异常"""
        driver = get_driver()
        driver.get(BASE_URL)
        driver.find_element(By.ID, "user-name").send_keys(USERS["error"])
        driver.find_element(By.ID, "password").send_keys(PASSWORD)
        driver.find_element(By.ID, "login-button").click()
        time.sleep(1)

        # 尝试加购不同商品
        buttons = driver.find_elements(By.CSS_SELECTOR, "[class*='btn_inventory']")
        for i, btn in enumerate(buttons):
            try:
                btn_text_before = btn.text
                btn.click()
                time.sleep(0.5)
                btn_text_after = btn.text
                if btn_text_before == btn_text_after:
                    print(f"  [BUG] error_user 第{i+1}个商品点击后按钮未变化: {btn_text_before}")
            except Exception as e:
                print(f"  [BUG] error_user 第{i+1}个商品报错: {e}")

        driver.quit()


# ============================================================
# 测试用例 5：退出登录
# ============================================================

class TestLogout:
    def test_logout(self):
        """TC-018：退出登录"""
        driver = get_driver()
        driver.get(BASE_URL)
        driver.find_element(By.ID, "user-name").send_keys(USERS["standard"])
        driver.find_element(By.ID, "password").send_keys(PASSWORD)
        driver.find_element(By.ID, "login-button").click()

        # 打开菜单
        driver.find_element(By.ID, "react-burger-menu-btn").click()
        time.sleep(0.5)
        driver.find_element(By.ID, "logout_sidebar_link").click()
        assert driver.current_url == BASE_URL, "退出后应回到登录页"
        print("[PASS] 退出登录成功，回到登录页")
        driver.quit()


# ============================================================
# 如果直接运行此脚本
# ============================================================
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--html=report.html"])
