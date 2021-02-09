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
        self.budget_detail.set_name(name)
        self.budget_detail.set_amount(amount)
        self.budget_detail.set_currency(currency)
        self.budget_detail.set_wallets(wallets)
        self.budget_detail.set_categories(categories)
        self.budget_detail.set_recurrence(recurrence)
        self.budget_detail.set_start_date(start_date)
        self.budget_detail.set_end_date(end_date)