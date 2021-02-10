from element_wrapper import ElementWrapper
from page_objects.budgets.budget_detail import BudgetDetail
from conftest import PLATFORM
from resolutions import Resolutions
from appium.webdriver.common.touch_action import TouchAction



class BudgetsGeneral():

    NAVIGATION_BUDGETS = "Navigation Budgets"
    ADD_BUDGET_BUTTON = "Add Budget Button"
    BUDGETS_HEADER = "Budgets Header"


    def __init__(self, driver):
        self.driver = driver
        self.action = TouchAction(self.driver)
        self.ew = ElementWrapper(self.driver)
        self.budget_detail = BudgetDetail(self.driver)
        self.rs = Resolutions(self.driver)

    def go_to_budgets(self):
        self.ew.wait_and_tap_element(self.NAVIGATION_BUDGETS, 30)
        self.ew.wait_till_element_is_visible(self.BUDGETS_HEADER, 10)

    def open_budget_create_screen(self):
        self.ew.wait_till_element_is_visible(self.BUDGETS_HEADER, 10)
        if PLATFORM == "Android":
            add_button_visible = self.ew.is_element_present(self.ADD_BUDGET_BUTTON)
            while add_button_visible is False:
                res = self.rs.get_resolution()
                self.action.long_press(None, self.rs.all_resolutions[f"{res}"]["x"],
                                       self.rs.all_resolutions[f"{res}"]["budget_overview_y_start"]) \
                    .move_to(None, self.rs.all_resolutions[f"{res}"]["x"],
                             self.rs.all_resolutions[f"{res}"]["budget_overview_y_end"]) \
                    .release().perform()
                add_button_visible = self.ew.is_element_present(self.ADD_BUDGET_BUTTON)
        else:
            add_button_visible = self.ew.get_attribute(self.ADD_BUDGET_BUTTON, "visible")
            while add_button_visible == "false":
                res = self.rs.get_resolution()
                self.driver.execute_script("mobile: dragFromToForDuration",
                                           {"duration": "0.1",
                                            "fromX": self.rs.all_resolutions[f"{res}"]["x"],
                                            "fromY": self.rs.all_resolutions[f"{res}"][
                                                "budget_overview_y_start"],
                                            "toX": self.rs.all_resolutions[f"{res}"]["x"],
                                            "toY": self.rs.all_resolutions[f"{res}"]["budget_overview_y_end"]})
                add_button_visible = self.ew.get_attribute(self.ADD_BUDGET_BUTTON, "visible")

        self.ew.wait_and_tap_element(self.ADD_BUDGET_BUTTON, 5)
        self.ew.wait_till_element_is_visible(self.budget_detail.BUDGET_HEADER, 10)

