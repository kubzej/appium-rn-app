from element_wrapper import ElementWrapper


class BankAccountDetail():

    CONSENT = "Consent"
    CONSENT_WEBVIEW = "Spendee"

    def __init__(self, driver):
        self.driver = driver
        self.ew = ElementWrapper(self.driver)

    def open_consent(self):
        self.ew.wait_and_tap_element(self.CONSENT, 15)
        self.ew.wait_till_element_is_not_visible(self.CONSENT, 10)

