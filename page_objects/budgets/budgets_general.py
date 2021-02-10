from element_wrapper import ElementWrapper
from page_objects.budgets.budget_detail import BudgetDetail

class BudgetsGeneral():

    NAVIGATION_BUDGETS = "Navigation Budgets"
    ADD_BUDGET_BUTTON = "Add Budget Button"
    BUDGETS_HEADER = "Budgets Header"
    BUDGET_ITEM = "Budget Item"

    def __init__(self, driver):
        self.driver = driver
        self.ew = ElementWrapper(self.driver)
        self.budget_detail = BudgetDetail(self.driver)

    def go_to_budgets(self):
        self.ew.wait_and_tap_element(self.NAVIGATION_BUDGETS, 30)
        self.ew.wait_till_element_is_visible(self.BUDGETS_HEADER, 10)

