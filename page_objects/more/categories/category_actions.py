from element_wrapper import ElementWrapper
from page_objects.more.categories.category_detail import CategoryDetail
from page_objects.more.more_general import MoreGeneral


class CategoryActions:

    ADD_CATEGORY_BUTTON = "Add Category Button"

    def __init__(self, driver):
        self.driver = driver
        self.category_detail = CategoryDetail(self.driver)
        self.ew = ElementWrapper(self.driver)
        self.more_general = MoreGeneral(self.driver)

    def open_category_create_screen(self):
        self.ew.wait_and_tap_element(self.ADD_CATEGORY_BUTTON, 10)
        self.ew.wait_till_element_is_visible(self.category_detail.CATEGORY_HEADER, 10)

    def create_category(self, name, color):
        self.open_category_create_screen()
        self.category_detail.set_name(name)
        self.category_detail.set_color(color)
