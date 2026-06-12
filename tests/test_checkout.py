"""结算流程测试"""
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


class TestCheckout:
    """结算模块测试用例"""

    def test_complete_checkout_flow(self, logged_in_driver):
        """完整结算流程：添加商品 → 购物车 → 填写信息 → 完成订单"""
        # 添加商品
        inv = InventoryPage(logged_in_driver)
        inv.add_first_product_to_cart()
        inv.go_to_cart()

        # 进入结算
        cart = CartPage(logged_in_driver)
        cart.go_to_checkout()

        # 填写收货信息
        checkout = CheckoutPage(logged_in_driver)
        checkout.fill_shipping_info("张三", "测试", "100000")
        checkout.click_continue()

        # 完成订单
        checkout.click_finish()
        assert "Thank you" in checkout.get_complete_message(), "应显示感谢信息"

    def test_checkout_empty_info_shows_error(self, logged_in_driver):
        """结算时信息缺失应提示错误"""
        inv = InventoryPage(logged_in_driver)
        inv.add_first_product_to_cart()
        inv.go_to_cart()

        cart = CartPage(logged_in_driver)
        cart.go_to_checkout()

        checkout = CheckoutPage(logged_in_driver)
        checkout.click_continue()
        error = checkout.get_error_message()
        assert "First Name is required" in error, f"应提示姓名为必填, 实际: {error}"
