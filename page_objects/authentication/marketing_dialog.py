from element_wrapper import ElementWrapper


class MarketingDialog:

    MARKETING_DIALOG = "Marketing Dialog"
    AGREE_BUTTON = "Agree"
    DISAGREE_BUTTON = "Don't Agree"

    def __init__(self, driver):
        self.driver = driver
        self.ew = ElementWrapper(self.driver)

    def agree_with_marketing(self):
        self.ew.wait_till_element_is_visible(self.MARKETING_DIALOG, 20)
        self.ew.wait_and_tap_element(self.AGREE_BUTTON, 5)

    def disagree_with_marketing(self):
        self.ew.wait_till_element_is_visible(self.MARKETING_DIALOG, 20)
        self.ew.wait_and_tap_element(self.DISAGREE_BUTTON, 5)


