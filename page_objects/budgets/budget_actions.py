from element_wrapper import ElementWrapper
from page_objects.budgets.budgets_general import BudgetsGeneral
from page_objects.budgets.budget_detail import BudgetDetail
from page_objects.budgets.budget_overview import BudgetOverview
from conftest import PLATFORM
from resolutions import Resolutions
from appium.webdriver.common.touch_action import TouchAction



class BudgetActions():
    def __init__(self, driver):
        self.driver = driver
        self.ew = ElementWrapper(self.driver)
        self.budgets_general = BudgetsGeneral(self.driver)
        self.budget_detail = BudgetDetail(self.driver)
        self.budget_overview = BudgetOverview(self.driver)
        self.rs = Resolutions(self.driver)
        self.action = TouchAction(self.driver)

    def create_budget(self, name, amount, currency, wallets, categories, recurrence, start_date, end_date):
        self.budgets_general.go_to_budgets()
        self.open_budget_create_screen()
        if name is not None:
            self.budget_detail.set_name(name)
        if amount is not None:
            self.budget_detail.set_amount(amount)
        if currency is not None:
            self.budget_detail.set_currency(currency)
        if wallets is not None:
            self.budget_detail.set_wallets(wallets)
        if categories is not None:
            self.budget_detail.set_categories(categories)
        if recurrence is not None:
            self.budget_detail.set_recurrence(recurrence)
        if start_date is not None:
            self.budget_detail.set_start_date(start_date)
        if end_date is not None:
            self.budget_detail.set_end_date(end_date)

    def save_budget(self):
        if self.driver.is_keyboard_shown():
            self.driver.hide_keyboard()
        self.ew.wait_and_tap_element(self.budget_detail.SAVE_BUDGET_BUTTON, 10)
        self.ew.wait_till_element_is_not_visible(self.budget_detail.SAVE_BUDGET_BUTTON, 10)

    def open_budget_create_screen(self):
        self.ew.wait_till_element_is_visible(self.budgets_general.BUDGETS_HEADER, 10)
        if PLATFORM == "Android":
            add_button_visible = self.ew.is_element_present(self.budgets_general.ADD_BUDGET_BUTTON)
            while add_button_visible is False:
                res = self.rs.get_resolution()
                self.action.long_press(None, self.rs.all_resolutions[f"{res}"]["x"],
                                       self.rs.all_resolutions[f"{res}"]["budget_overview_y_start"]) \
                    .move_to(None, self.rs.all_resolutions[f"{res}"]["x"],
                             self.rs.all_resolutions[f"{res}"]["budget_overview_y_end"]) \
                    .release().perform()
                add_button_visible = self.ew.is_element_present(self.budgets_general.ADD_BUDGET_BUTTON)
        else:
            add_button_visible = self.ew.get_attribute(self.budgets_general.ADD_BUDGET_BUTTON, "visible")
            while add_button_visible == "false":
                res = self.rs.get_resolution()
                self.driver.execute_script("mobile: dragFromToForDuration",
                                           {"duration": "0.1",
                                            "fromX": self.rs.all_resolutions[f"{res}"]["x"],
                                            "fromY": self.rs.all_resolutions[f"{res}"][
                                                "budget_overview_y_start"],
                                            "toX": self.rs.all_resolutions[f"{res}"]["x"],
                                            "toY": self.rs.all_resolutions[f"{res}"]["budget_overview_y_end"]})
                add_button_visible = self.ew.get_attribute(self.budgets_general.ADD_BUDGET_BUTTON, "visible")

        self.ew.wait_and_tap_element(self.budgets_general.ADD_BUDGET_BUTTON, 5)
        self.ew.wait_till_element_is_visible(self.budget_detail.BUDGET_HEADER, 10)

    def open_budget(self):
        self.budgets_general.go_to_budgets()
        self.ew.wait_till_element_is_visible(self.budgets_general.BUDGETS_HEADER, 5)
        if self.ew.is_element_present(self.budgets_general.BUDGET_ITEM) is False:
            self.create_budget(name="random", amount="random", currency=None, wallets=None, categories=None,
                                              recurrence=None, start_date=None, end_date=None)
            self.save_budget()
            self.budgets_general.go_to_budgets()
        self.ew.wait_and_tap_element(self.budgets_general.BUDGET_ITEM, 5)
        self.ew.wait_and_tap_element(self.budget_overview.BUDGET_SETTINGS_BUTTON, 5)
        self.ew.wait_till_element_is_visible(self.budget_detail.BUDGET_HEADER, 5)

    def edit_budget(self, name, amount, currency, wallets, categories, recurrence, start_date, end_date):
        self.open_budget()
        if name is not None:
            if PLATFORM == "Android":
                self.ew.get_element(self.budget_detail.NAME_INPUT).clear()
            else:
                self.ew.get_element(self.budget_detail.SELECTED_NAME_IOS).clear()
            self.budget_detail.set_name(name)
        if amount is not None:
            self.ew.wait_and_tap_element(self.budget_detail.AMOUNT_INPUT, 5)
            self.ew.wait_till_element_is_visible(self.budget_detail.NUMPAD_CLEAR, 10)
            for i in range(6):
                self.ew.tap_element(self.budget_detail.NUMPAD_CLEAR)
            self.ew.tap_element(self.budget_detail.NUMPAD_BACKDROP)
            self.budget_detail.set_amount(amount)
        if currency is not None:
            self.budget_detail.set_currency(currency)
        if wallets is not None:
            self.budget_detail.set_wallets(wallets)
        if categories is not None:
            self.budget_detail.set_categories(categories)
        if recurrence is not None:
            self.budget_detail.set_recurrence(recurrence)
        if start_date is not None:
            self.budget_detail.set_start_date(start_date)
        if end_date is not None:
            self.budget_detail.set_end_date(end_date)

    def delete_budget(self):
        self.ew.wait_and_tap_element(self.budget_detail.TRASH_ICON, 10)
        self.ew.wait_and_tap_element(self.budget_detail.DELETE_BUTTON, 10)
        self.ew.wait_till_element_is_visible(self.budgets_general.BUDGETS_HEADER, 10)


