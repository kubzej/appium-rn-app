import time

from appium.webdriver.common.touch_action import TouchAction

from conftest import PLATFORM
from element_wrapper import ElementWrapper
from page_objects.wallets.wallet_detail import WalletDetail
from page_objects.wallets.wallet_overview import WalletOverview
from page_objects.wallets.wallets_general import WalletsGeneral
from resolutions import Resolutions


class WalletValidator:

    def __init__(self, driver):
        self.driver = driver
        self.action = TouchAction(self.driver)
        self.ew = ElementWrapper(self.driver)
        self.rs = Resolutions(self.driver)
        self.wallet_detail = WalletDetail(self.driver)
        self.wallet_overview = WalletOverview(self.driver)
        self.wallets_general = WalletsGeneral(self.driver)

    def get_all_attributes(self):
        """ Getting all attributes of wallet
        :return: dict
        """
        all_attributes = {"name": self.wallet_detail.get_name(),
                          "amount": self.wallet_detail.get_amount(),
                          "currency": self.wallet_detail.get_currency(),
                          "categories": self.wallet_detail.get_categories(),
                          }

        return all_attributes

    def is_wallet_existing(self, attributes):
        """ Checking if wallet is visible inside Wallets section
        :param attributes: dict
        :return: bool
        """
        wallet_locator = f"cash/" \
                         f"{attributes['name']}/" \
                         f"{attributes['amount']}/" \
                         f"{self.adjust_currency(attributes['currency'])[0]}/" \
                         f"{self.adjust_currency(attributes['currency'])[1]}/" \
                         f"{attributes['categories']}"

        print(f'ATTRIBUTES: {attributes}')
        print(f'LOCATOR: {wallet_locator}')

        if self.ew.is_element_present(self.wallet_overview.BACK_BUTTON):
            self.ew.tap_element(self.wallet_overview.BACK_BUTTON)
            self.ew.wait_till_element_is_visible(self.wallets_general.WALLETS_ANIMATED_HEADER, 10)

        android_timeout = time.time() + 30
        ios_timeout = time.time() + 5
        res = self.rs.get_resolution()
        is_wallet_present = self.ew.is_element_present(wallet_locator)
        while is_wallet_present is False:
            if PLATFORM == "Android":
                self.action.long_press(None, self.rs.all_resolutions[f"{res}"]["x"],
                                       self.rs.all_resolutions[f"{res}"]["wallets_overview_y_start"]) \
                    .move_to(None, self.rs.all_resolutions[f"{res}"]["x"],
                             self.rs.all_resolutions[f"{res}"]["wallets_overview_y_end"]) \
                    .release().perform()
                is_wallet_present = self.ew.is_element_present(wallet_locator)
                if time.time() > android_timeout:
                    return False
            else:
                is_wallet_present = self.ew.is_element_present(wallet_locator)
                if time.time() > ios_timeout:
                    return False
        return True

    def adjust_currency(self, currency):
        """ Adjusting currency for wallet locator
        :param currency: str
        :return:
        """
        if currency == "USD":
            return [currency, "undefined"]
        else:
            return ["USD", currency]
