"""登录功能测试"""
import pytest
from pages.login_page import LoginPage


class TestLogin:
    """登录模块测试用例"""

    def test_login_success(self, driver):
        """正确账号密码登录成功，跳转至商品列表页"""
        login_page = LoginPage(driver).open()
        login_page.login("standard_user", "secret_sauce")
        assert "inventory" in driver.current_url, "登录成功后应跳转到商品页"

    def test_login_wrong_password(self, driver):
        """错误密码登录失败，显示错误提示"""
        login_page = LoginPage(driver).open()
        login_page.login("standard_user", "wrong_password")
        error = login_page.get_error_message()
        assert "not match" in error.lower(), f"应提示密码错误, 实际: {error}"

    def test_login_empty_username(self, driver):
        """空用户名登录失败"""
        login_page = LoginPage(driver).open()
        login_page.login("", "secret_sauce")
        error = login_page.get_error_message()
        assert "Username is required" in error, f"应提示用户名为空, 实际: {error}"

    def test_login_locked_user(self, driver):
        """锁定账号登录失败"""
        login_page = LoginPage(driver).open()
        login_page.login("locked_out_user", "secret_sauce")
        error = login_page.get_error_message()
        assert "locked out" in error.lower(), f"应提示账号被锁定, 实际: {error}"
