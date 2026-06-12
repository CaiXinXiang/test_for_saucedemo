"""购物车功能测试"""
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


class TestCart:
    """购物车模块测试用例"""

    def test_cart_page_empty(self, logged_in_driver):
        """空购物车进入购物车页"""
        page = InventoryPage(logged_in_driver)
        page.go_to_cart()
        cart = CartPage(logged_in_driver)
        assert cart.get_title() == "Your Cart", "标题应为 Your Cart"
        assert cart.get_cart_item_count() == 0, "购物车应为空"

    def test_remove_item_from_cart(self, logged_in_driver):
        """从购物车移除商品"""
        page = InventoryPage(logged_in_driver)
        page.add_first_product_to_cart()
        page.go_to_cart()
        cart = CartPage(logged_in_driver)
        assert cart.get_cart_item_count() == 1, "应有1件商品"
        cart.remove_first_item()
        assert cart.get_cart_item_count() == 0, "移除后购物车应为空"
