from element_wrapper import ElementWrapper
from page_objects.budgets.budgets_general import BudgetsGeneral
from page_objects.budgets.budget_detail import BudgetDetail

class BudgetActions():
    def __init__(self, driver):
        self.driver = driver
        self.ew = ElementWrapper(self.driver)
        self.budgets_general = BudgetsGeneral(self.driver)
        self.budget_detail = BudgetDetail(self.driver)

    def create_budget(self, name, amount, currency, wallets, categories, recurrence, start_date, end_date):
        self.budgets_general.go_to_budgets()
        self.budgets_general.open_budget_create_screen()
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
            print('jde to tudy')
            self.driver.hide_keyboard()
        self.ew.wait_and_tap_element(self.budget_detail.SAVE_BUDGET_BUTTON, 10)


