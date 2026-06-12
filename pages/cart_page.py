from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    """购物车页"""

    PAGE_TITLE = (By.CLASS_NAME, "title")
    CART_ITEMS = (By.CSS_SELECTOR, ".cart_item")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "button.cart_button")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")

    def get_title(self):
        return self.get_text(self.PAGE_TITLE)

    def get_cart_item_count(self):
        return len(self.driver.find_elements(*self.CART_ITEMS))

    def remove_first_item(self):
        self.click(self.REMOVE_BUTTONS)

    def go_to_checkout(self):
        self.click(self.CHECKOUT_BUTTON)

    def continue_shopping(self):
        self.click(self.CONTINUE_SHOPPING_BUTTON)
