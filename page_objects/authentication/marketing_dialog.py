from element_wrapper import ElementWrapper


class MarketingDialog:
    MARKETING_DIALOG = "Marketing Dialog"
    AGREE_BUTTON = "Agree"
    DISAGREE_BUTTON = "Don't Agree"
    ALLOW_BUTTON = 'Allow'

    def __init__(self, driver):
        self.driver = driver
        self.ew = ElementWrapper(self.driver)

    def agree_with_marketing(self):
        """Clicks on agree button on marketing dialog"""
        self.ew.wait_till_element_is_visible(self.MARKETING_DIALOG, 20)
        self.ew.wait_and_tap_element(self.AGREE_BUTTON, 5)

    def disagree_with_marketing(self):
        """Clicks on disagree button on marketing dialog"""
        self.ew.wait_till_element_is_visible(self.MARKETING_DIALOG, 20)
        self.ew.wait_and_tap_element(self.DISAGREE_BUTTON, 5)

    def agree_with_ios_notifications(self):
        """Clicks on agree button on ios notifications dialog"""
        if self.ew.is_element_present(self.ALLOW_BUTTON):
            self.ew.wait_and_tap_element(self.ALLOW_BUTTON, 30)
