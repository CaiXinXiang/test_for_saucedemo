from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class InventoryPage(BasePage):
    """商品列表页"""

    PAGE_TITLE = (By.CLASS_NAME, "title")
    SORT_DROPDOWN = (By.CSS_SELECTOR, "[data-test='product-sort-container']")
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".inventory_item_name")
    PRODUCT_PRICES = (By.CSS_SELECTOR, ".inventory_item_price")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "button.btn_inventory")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")

    def get_title(self):
        return self.get_text(self.PAGE_TITLE)

    def get_product_count(self):
        return len(self.driver.find_elements(*self.PRODUCT_NAMES))

    def sort_by(self, option_value):
        from selenium.webdriver.support.ui import Select
        select = Select(self.driver.find_element(*self.SORT_DROPDOWN))
        select.select_by_value(option_value)

    def get_all_product_names(self):
        return [el.text for el in self.driver.find_elements(*self.PRODUCT_NAMES)]

    def get_all_product_prices(self):
        return [float(el.text.replace("$", "")) for el in self.driver.find_elements(*self.PRODUCT_PRICES)]

    def add_first_product_to_cart(self):
        self.click(self.ADD_TO_CART_BUTTONS)

    def add_product_by_index(self, index):
        buttons = self.driver.find_elements(*self.ADD_TO_CART_BUTTONS)
        self.driver.execute_script("arguments[0].click();", buttons[index])

    def get_cart_count(self):
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            badge = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located(self.CART_BADGE)
            )
            return int(badge.text)
        except Exception:
            return 0

    def go_to_cart(self):
        self.click(self.CART_LINK)
