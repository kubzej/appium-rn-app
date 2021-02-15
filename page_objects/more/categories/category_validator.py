from appium.webdriver.common.touch_action import TouchAction
from conftest import PLATFORM
from element_wrapper import ElementWrapper
from resolutions import Resolutions
from page_objects.more.categories.category_detail import CategoryDetail
import time


class CategoryValidator:

    def __init__(self, driver):
        self.driver = driver
        self.category_detail = CategoryDetail(self.driver)
        self.action = TouchAction(self.driver)
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