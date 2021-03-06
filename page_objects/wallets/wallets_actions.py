from appium.webdriver.common.touch_action import TouchAction

from conftest import PLATFORM
from element_wrapper import ElementWrapper
from page_objects.wallets.wallet_detail import WalletDetail
from page_objects.wallets.wallet_overview import WalletOverview
from page_objects.wallets.wallets_general import WalletsGeneral
from resolutions import Resolutions


class WalletsActions:

    def __init__(self, driver):
        self.driver = driver
        self.action = TouchAction(self.driver)
        self.ew = ElementWrapper(self.driver)
        self.rs = Resolutions(self.driver)
        self.wallets_general = WalletsGeneral(self.driver)
        self.wallet_detail = WalletDetail(self.driver)
        self.wallets_overview = WalletOverview(self.driver)

    def create_wallet(self, name, amount, currency, categories):
        """ Opens wallet create screen and sets requested attributes
        :param name: str or None
        :param amount: str or None
        :param currency: str or None
        :param categories: str or int or None
        """
        self.wallets_general.go_to_wallets()
        self.open_wallet_create_screen()
        self.wallet_detail.set_name(name)
        if amount is not None:
            self.wallet_detail.set_amount(amount)
        if currency is not None:
            self.wallet_detail.set_currency(currency)
        if categories is not None:
            self.wallet_detail.set_categories(categories)

    def open_wallet_create_screen(self):
        """Opens wallet create screen"""
        self.ew.wait_till_element_is_visible(self.wallets_general.WALLETS_ANIMATED_HEADER, 10)

        if PLATFORM == "Android":
            add_button_visible = self.ew.is_element_present(self.wallets_general.ADD_WALLET_BUTTON)
            while add_button_visible is False:
                res = self.rs.get_resolution()
                self.action.long_press(None, self.rs.all_resolutions[f"{res}"]["x"],
                                       self.rs.all_resolutions[f"{res}"]["wallets_overview_y_start"]) \
                    .move_to(None, self.rs.all_resolutions[f"{res}"]["x"],
                             self.rs.all_resolutions[f"{res}"]["wallets_overview_y_end"]) \
                    .release().perform()
                add_button_visible = self.ew.is_element_present(self.wallets_general.ADD_WALLET_BUTTON)
        else:
            add_button_visible = self.ew.get_attribute(self.wallets_general.ADD_WALLET_BUTTON, "visible")
            while add_button_visible == "false":
                res = self.rs.get_resolution()
                self.driver.execute_script("mobile: dragFromToForDuration",
                                           {"duration": "0.1",
                                            "fromX": self.rs.all_resolutions[f"{res}"]["x"],
                                            "fromY": self.rs.all_resolutions[f"{res}"][
                                                "wallets_overview_y_start"],
                                            "toX": self.rs.all_resolutions[f"{res}"]["x"],
                                            "toY": self.rs.all_resolutions[f"{res}"]["wallets_overview_y_end"]})
                add_button_visible = self.ew.get_attribute(self.wallets_general.ADD_WALLET_BUTTON, "visible")

        self.ew.wait_and_tap_element(self.wallets_general.ADD_WALLET_BUTTON, 5)
        self.ew.wait_till_element_is_visible(self.wallet_detail.WALLET_HEADER, 10)

    def save_wallet(self):
        """Clicks on save wallet button"""
        if self.driver.is_keyboard_shown():
            self.driver.hide_keyboard()
        self.ew.wait_and_tap_element(self.wallet_detail.SAVE_WALLET_BUTTON, 10)
        self.ew.wait_till_element_is_not_visible(self.wallet_detail.SAVE_WALLET_BUTTON, 10)

    def open_wallet(self):
        """Opens existing wallet"""
        self.wallets_general.go_to_wallets()
        self.ew.wait_till_element_is_visible(self.wallets_general.WALLETS_ANIMATED_HEADER, 10)
        self.ew.wait_and_tap_element(self.wallets_general.WALLET_ITEM, 5)
        self.ew.wait_and_tap_element(self.wallets_overview.EDIT_BUTTON, 5)
        self.ew.wait_till_element_is_visible(self.wallet_detail.WALLET_HEADER, 5)

    def edit_wallet(self, name, amount, currency, categories):
        """Changes requested attributes of wallet
        :param name: str or None
        :param amount: str or None
        :param currency: str or None
        :param categories: str or int or None
        """
        self.open_wallet()
        if name is not None:
            if PLATFORM == "Android":
                self.ew.get_element(self.wallet_detail.NAME_INPUT).clear()
            else:
                self.ew.get_element(self.wallet_detail.SELECTED_NAME_IOS).clear()
            self.wallet_detail.set_name(name)
        if amount is not None:
            self.ew.wait_and_tap_element(self.wallet_detail.AMOUNT_INPUT, 5)
            self.ew.wait_till_element_is_visible(self.wallet_detail.NUMPAD_CLEAR, 10)
            for i in range(6):
                self.ew.tap_element(self.wallet_detail.NUMPAD_CLEAR)
            self.ew.tap_element(self.wallet_detail.NUMPAD_BACKDROP)
            self.wallet_detail.set_amount(amount)
        if currency is not None:
            self.wallet_detail.set_currency(currency)
        if categories is not None:
            self.wallet_detail.set_categories(categories)

    def delete_wallet(self):
        """Deletes wallet from wallet detail"""
        self.ew.wait_and_tap_element(self.wallet_detail.TRASH_ICON, 10)
        self.ew.wait_and_tap_element(self.wallet_detail.DELETE_BUTTON, 10)
        self.ew.wait_till_element_is_visible(self.wallets_general.WALLETS_ANIMATED_HEADER, 10)

    def invite_user_to_wallet(self):
        """Opens wallet and invitation screen"""
        self.open_wallet()
        self.wallet_detail.invite_user()
