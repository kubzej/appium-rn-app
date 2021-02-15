from element_wrapper import ElementWrapper
from page_objects.more.categories.category_detail import CategoryDetail
from page_objects.more.more_general import MoreGeneral
import random


class CategoryActions:

    ADD_CATEGORY_BUTTON = "Add Category Button"
    CATEGORY_ITEM = "Category Item"

    # TYPE
    EXPENSES = "Expenses"
    INCOME = "Income"


    def __init__(self, driver):
        self.driver = driver
        self.category_detail = CategoryDetail(self.driver)
        self.ew = ElementWrapper(self.driver)
        self.more_general = MoreGeneral(self.driver)

    def set_type(self, type_of_category):
        if type_of_category == "random":
            type_of_category = random.choice([self.EXPENSES, self.INCOME])
        elif type_of_category == "expenses":
            type_of_category = self.EXPENSES
        else:
            type_of_category = self.INCOME

        self.ew.wait_and_tap_element(type_of_category, 5)

    def open_category_create_screen(self):
        self.ew.wait_and_tap_element(self.ADD_CATEGORY_BUTTON, 10)
        self.ew.wait_till_element_is_visible(self.category_detail.CATEGORY_HEADER, 10)

    def open_category(self):
        if self.ew.is_element_present(self.CATEGORY_ITEM) is False:
            self.create_category(type_of_category="random", name="random", color="random", image="random")
            self.save_category()

        self.ew.wait_and_tap_element(self.CATEGORY_ITEM, 10)
        self.ew.wait_till_element_is_visible(self.category_detail.CATEGORY_HEADER, 10)

    def create_category(self, type_of_category, name, color, image):
        self.set_type(type_of_category)
        self.open_category_create_screen()
        self.category_detail.set_name(name)
        self.category_detail.set_color(color)
        self.category_detail.set_image(image)

    def save_category(self):
        self.ew.wait_and_tap_element(self.category_detail.SAVE_CATEGORY_BUTTON, 10)
        self.ew.wait_till_element_is_visible(self.more_general.CATEGORIES_HEADER, 10)

    def edit_category(self, type_of_category, name, color, image):
        self.set_type(type_of_category)
        self.open_category()
        if name is not None:
            self.category_detail.set_name(name)
        if color is not None:
            self.category_detail.set_color(color)
        if image is not None:
            self.category_detail.set_image(image)

