import time

from appium.webdriver.common.touch_action import TouchAction

from conftest import PLATFORM
from element_wrapper import ElementWrapper
from page_objects.more.categories.categories_general import CategoriesGeneral
from page_objects.more.categories.category_detail import CategoryDetail
from resolutions import Resolutions


class CategoryValidator:

    def __init__(self, driver):
        self.driver = driver
        self.action = TouchAction(self.driver)
        self.categories_general = CategoriesGeneral(self.driver)
        self.category_detail = CategoryDetail(self.driver)
        self.ew = ElementWrapper(self.driver)
        self.rs = Resolutions(self.driver)

    def get_all_attributes(self):
        all_attributes = {"name": self.category_detail.get_name(),
                          "color": self.category_detail.get_color(),
                          "image": self.category_detail.get_image()
                          }

        return all_attributes

    def is_category_existing(self, attributes):
        category_locator = f"{attributes['name']}/" \
                           f"{attributes['color']}/" \
                           f"{attributes['image']}"

        print(f'ATTRIBUTES: {attributes}')
        print(f'LOCATOR: {category_locator}')

        android_timeout = time.time() + 30
        ios_timeout = time.time() + 5
        res = self.rs.get_resolution()
        is_category_present = self.ew.is_element_present(category_locator)
        while is_category_present is False:
            if PLATFORM == "Android":
                self.action.long_press(None, self.rs.all_resolutions[f"{res}"]["x"],
                                       self.rs.all_resolutions[f"{res}"]["categories_y_start"]) \
                    .move_to(None, self.rs.all_resolutions[f"{res}"]["x"],
                             self.rs.all_resolutions[f"{res}"]["categories_y_end"]) \
                    .release().perform()
                is_category_present = self.ew.is_element_present(category_locator)
                if time.time() > android_timeout:
                    return False
            else:
                is_category_present = self.ew.is_element_present(category_locator)
                if time.time() > ios_timeout:
                    return False
        return True

    def get_selected_categories(self):
        categories = self.ew.get_attributes(self.categories_general.CATEGORY_INFO, "content-desc")
        name1, color1, image1 = categories[0].split('/')
        attributes1 = {
            "name": name1,
            "color": color1,
            "image": image1
        }
        name2, color2, image2 = categories[1].split('/')
        attributes2 = {
            "name": name2,
            "color": color2,
            "image": image2
        }
        return (attributes1, attributes2)
