import random

from element_wrapper import ElementWrapper


class BankAccountDetail():
    CONSENT = "Consent"
    CONSENT_WEBVIEW = "Spendee"
    REMOVE_BUTTON = "Remove Button"
    REMOVE_CONFIRM = "Remove"
    EYE_ICON = "Eye Icon-true"
    BACK_BUTTON = "Back Button"

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

    def hide_bank_wallets(self, wallets):
        if wallets == "random":
            wallets = random.randint(1, 3)

        x = 0
        all_wallets = self.ew.get_elements(self.EYE_ICON)
        for i in all_wallets:
            x = x + 1
            if x <= wallets:
                i.click()
