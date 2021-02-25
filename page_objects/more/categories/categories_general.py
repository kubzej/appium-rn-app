import random

from element_wrapper import ElementWrapper


class CategoriesGeneral():
    ADD_CATEGORY_BUTTON = "Add Category Button"
    MERGE_CATEGORIES_BUTTON = "Merge Categories Button"
    CATEGORY_ITEM = "Category Item"
    CATEGORY_INFO = '//android.view.ViewGroup[@content-desc="Category Item"]/android.view.ViewGroup'
    CONFIRM_MERGE_BUTTON = "Merge"

    # TYPE
    EXPENSES = "Expenses"
    INCOME = "Income"

    def __init__(self, driver):
        self.driver = driver
        self.ew = ElementWrapper(self.driver)

    def set_type(self, type_of_category):
        """ Selects income or expense set of categories
        :param type_of_category: str
        """
        if type_of_category == "random":
            type_of_category = random.choice([self.EXPENSES, self.INCOME])
        elif type_of_category == "expenses":
            type_of_category = self.EXPENSES
        else:
            type_of_category = self.INCOME

        self.ew.wait_and_tap_element(type_of_category, 5)
