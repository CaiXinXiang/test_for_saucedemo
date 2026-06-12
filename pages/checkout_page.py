from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """结算页"""

    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    FINISH_BUTTON = (By.ID, "finish")
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    ITEM_TOTAL_LABEL = (By.CLASS_NAME, "summary_subtotal_label")

    def fill_shipping_info(self, first_name, last_name, postal_code):
        self.input_text(self.FIRST_NAME_INPUT, first_name)
        self.input_text(self.LAST_NAME_INPUT, last_name)
        self.input_text(self.POSTAL_CODE_INPUT, postal_code)

    def click_continue(self):
        self.click(self.CONTINUE_BUTTON)

    def click_finish(self):
        self.click(self.FINISH_BUTTON)

    def get_complete_message(self):
        return self.get_text(self.COMPLETE_HEADER)

    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)

    def get_item_total(self):
        return self.get_text(self.ITEM_TOTAL_LABEL)
