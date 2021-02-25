from element_wrapper import ElementWrapper
from page_objects.more.categories.categories_general import CategoriesGeneral
from page_objects.more.categories.category_detail import CategoryDetail
from page_objects.more.more_general import MoreGeneral


class CategoryActions:

    def __init__(self, driver):
        self.driver = driver
        self.category_detail = CategoryDetail(self.driver)
        self.categories_general = CategoriesGeneral(self.driver)
        self.ew = ElementWrapper(self.driver)
        self.more_general = MoreGeneral(self.driver)

    def open_category_create_screen(self):
        self.ew.wait_and_tap_element(self.categories_general.ADD_CATEGORY_BUTTON, 10)
        self.ew.wait_till_element_is_visible(self.category_detail.CATEGORY_HEADER, 10)

    def open_category(self):
        if self.ew.is_element_present(self.categories_general.CATEGORY_ITEM) is False:
            self.create_category(type_of_category="random", name="random", color="random", image="random")
            self.save_category()

        self.ew.wait_and_tap_element(self.categories_general.CATEGORY_ITEM, 10)
        self.ew.wait_till_element_is_visible(self.category_detail.CATEGORY_HEADER, 10)

    def create_category(self, type_of_category, name, color, image):
        self.categories_general.set_type(type_of_category)
        self.open_category_create_screen()
        self.category_detail.set_name(name)
        self.category_detail.set_color(color)
        self.category_detail.set_image(image)

    def save_category(self):
        self.ew.wait_and_tap_element(self.category_detail.SAVE_CATEGORY_BUTTON, 10)
        self.ew.wait_till_element_is_visible(self.more_general.CATEGORIES_HEADER, 10)

    def confirm_merge(self):
        self.ew.wait_and_tap_element(self.categories_general.MERGE_CATEGORIES_BUTTON, 10)
        self.ew.wait_and_tap_element(self.categories_general.CONFIRM_MERGE_BUTTON, 10)
        self.ew.wait_till_element_is_visible(self.more_general.CATEGORIES_HEADER, 10)

    def edit_category(self, type_of_category, name, color, image):
        self.categories_general.set_type(type_of_category)
        self.open_category()
        if name is not None:
            self.category_detail.set_name(name)
        if color is not None:
            self.category_detail.set_color(color)
        if image is not None:
            self.category_detail.set_image(image)

    def delete_category(self):
        self.ew.wait_and_tap_element(self.category_detail.TRASH_ICON, 10)
        self.ew.wait_and_tap_element(self.category_detail.DELETE_BUTTON, 10)
        self.ew.wait_till_element_is_visible(self.more_general.CATEGORIES_HEADER, 10)

    def merge_categories(self):
        self.ew.wait_and_tap_element(self.categories_general.MERGE_CATEGORIES_BUTTON, 10)
        all_visible_categories = self.ew.get_attributes(self.categories_general.CATEGORY_INFO, "content-desc")
        self.ew.tap_element(all_visible_categories[0])
        self.ew.tap_element(all_visible_categories[1])
