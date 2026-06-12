"""商品列表功能测试"""
from pages.inventory_page import InventoryPage


class TestInventory:
    """商品列表模块测试用例"""

    def test_product_list_displayed(self, logged_in_driver):
        """商品列表正常加载，展示6个商品"""
        page = InventoryPage(logged_in_driver)
        assert page.get_title() == "Products", "页面标题应为 Products"
        assert page.get_product_count() == 6, f"商品数量应为6, 实际: {page.get_product_count()}"

    def test_sort_by_name_asc(self, logged_in_driver):
        """按名称 A→Z 排序"""
        page = InventoryPage(logged_in_driver)
        page.sort_by("az")
        names = page.get_all_product_names()
        assert names == sorted(names), f"名称应升序排列, 实际: {names}"

    def test_sort_by_price_desc(self, logged_in_driver):
        """按价格高→低排序"""
        page = InventoryPage(logged_in_driver)
        page.sort_by("hilo")
        prices = page.get_all_product_prices()
        assert prices == sorted(prices, reverse=True), f"价格应降序排列, 实际: {prices}"

    def test_add_to_cart_updates_badge(self, logged_in_driver):
        """添加商品后购物车徽标数字更新"""
        page = InventoryPage(logged_in_driver)
        assert page.get_cart_count() == 0, "初始购物车应为空"
        page.add_first_product_to_cart()
        assert page.get_cart_count() == 1, "添加1件商品后徽标应为1"
        page.add_product_by_index(1)
        assert page.get_cart_count() == 2, "添加第2件商品后徽标应为2"
