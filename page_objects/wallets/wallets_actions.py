from element_wrapper import ElementWrapper
from page_objects.wallets.wallets_general import WalletsGeneral
from page_objects.wallets.wallet_detail import WalletDetail
from conftest import PLATFORM
from resolutions import Resolutions
from appium.webdriver.common.touch_action import TouchAction


class WalletsActions:

    def __init__(self, driver):
        self.driver = driver
        self.action = TouchAction(self.driver)
        self.ew = ElementWrapper(self.driver)
        self.rs = Resolutions(self.driver)
        self.wallets_general = WalletsGeneral(self.driver)
        self.wallet_detail = WalletDetail(self.driver)

    def create_wallet(self, name, amount, currency, categories):
        self.wallets_general.go_to_wallets()
        self.open_wallet_create_screen()
        self.wallet_detail.set_name(name)
        self.wallet_detail.set_amount(amount)
        if currency is not None:
            self.wallet_detail.set_currency(currency)
        if categories is not None:
            self.wallet_detail.set_categories(categories)

    def open_wallet_create_screen(self):
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
