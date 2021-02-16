from element_wrapper import ElementWrapper


class BankAccountDetail():

    CONSENT = "Consent"
    CONSENT_WEBVIEW = "Spendee"
    REMOVE_BUTTON = "Remove Button"
    REMOVE_CONFIRM = "Remove"

    def __init__(self, driver):
        self.driver = driver
        self.ew = ElementWrapper(self.driver)

    def open_consent(self):
        self.ew.wait_and_tap_element(self.CONSENT, 15)
        self.ew.wait_till_element_is_not_visible(self.CONSENT, 10)

    def disconnect_bank_account(self):
        self.ew.wait_and_tap_element(self.REMOVE_BUTTON, 15)
        self.ew.wait_and_tap_element(self.REMOVE_CONFIRM, 5)
        self.ew.wait_till_element_is_not_visible(self.REMOVE_CONFIRM, 10)


