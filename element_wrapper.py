import logging
import time

from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException

from conftest import PLATFORM
from resolutions import Resolutions


class ElementWrapper:

    def __init__(self, driver):
        self.driver = driver
        self.action = TouchAction(self.driver)
        self.log = logging.getLogger('log')
        self.rs = Resolutions(self.driver)

    def get_by_type(self, locator):
        if str(locator).startswith("//") or str(locator).startswith("(//"):
            return MobileBy.XPATH
        elif str(locator).startswith("com.android"):
            return MobileBy.ID
        elif str(locator).startswith("android:id"):
            return MobileBy.ID
        elif str(locator).startswith('label'):
            return MobileBy.IOS_PREDICATE
        elif str(locator).startswith('**'):
            return MobileBy.IOS_CLASS_CHAIN
        else:
            return MobileBy.ACCESSIBILITY_ID

    def get_element(self, locator):
        by_type = self.get_by_type(locator)
        element = self.driver.find_element(by_type, locator)
        return element

    def get_elements(self, locator):
        by_type = self.get_by_type(locator)
        element_list = self.driver.find_elements(by_type, locator)
        if len(element_list) < 1 or element_list is None:
            self.log.error(f"element_list {locator} NOT found")
        return element_list

    def is_element_present(self, locator):
        try:
            element = self.get_element(locator)
            if element is not None:
                self.log.info(f"element {locator} found")
                return True
            else:
                return False
        except NoSuchElementException:
            self.log.info(f"element {locator} NOT found")
            return False

    def are_elements_present(self, locator):
        element_list = self.get_elements(locator)
        if len(element_list) > 0:
            self.log.info(f"element_list {locator} found")
            return True
        else:
            self.log.info(f"element list {locator} NOT found")
            return False

    def get_text_of_element(self, locator):
        try:
            element = self.get_element(locator)
            return element.text
        except NoSuchElementException:
            self.log.info(f"element {locator} NOT found, can't get the text of element")

    def get_text_of_elements(self, locator):
        try:
            element_list = self.get_elements(locator)
            texts = []
            for i in element_list:
                texts.append(i.text)
            return texts
        except NoSuchElementException:
            self.log.info(f"elements {locator} NOT found, can't get the text of elements")

    def wait_till_element_is_visible(self, locator, timeout_seconds):
        timeout = time.time() + timeout_seconds
        visibility_of_element = self.is_element_present(locator)
        while visibility_of_element is False:
            time.sleep(0.1)
            visibility_of_element = self.is_element_present(locator)
            if time.time() > timeout:
                raise NoSuchElementException(f"element {locator} NOT found")

    def wait_till_element_is_not_visible(self, locator, timeout_seconds):
        timeout = time.time() + timeout_seconds
        visibility_of_element = self.is_element_present(locator)
        while visibility_of_element is True:
            time.sleep(0.1)
            visibility_of_element = self.is_element_present(locator)
            if time.time() > timeout:
                raise NoSuchElementException(f"element {locator} dont't disappeared")

    def tap_element(self, locator):
        self.action.tap(self.get_element(locator)).perform()

    def wait_and_tap_element(self, locator, timeout_seconds):
        self.wait_till_element_is_visible(locator, timeout_seconds)
        self.action.tap(self.get_element(locator)).perform()

    def get_attribute(self, locator, attribute):
        byType = self.get_by_type(locator)
        return self.driver.find_element(byType, locator).get_attribute(attribute)

    def get_attributes(self, locator, attribute):
        by_type = self.get_by_type(locator)
        element_list = self.driver.find_elements(by_type, locator)
        attributes = []
        for i in element_list:
            attributes.append(i.get_attribute(attribute))
        return attributes

    def swipe_if_element_not_present(self, locator):
        element_present = self.is_element_present(locator)
        timeout = time.time() + 30
        while element_present is False:
            res = self.rs.get_resolution()
            if PLATFORM == "Android":
                self.action.long_press(None, self.rs.all_resolutions[f"{res}"]["x"],
                                       self.rs.all_resolutions[f"{res}"]["element_not_present_swipe_y_start"]) \
                    .move_to(None, self.rs.all_resolutions[f"{res}"]["x"],
                             self.rs.all_resolutions[f"{res}"]["element_not_present_swipe_y_end"]) \
                    .release().perform()
            else:
                self.driver.execute_script("mobile: dragFromToForDuration",
                                           {"duration": "0.1",
                                            "fromX": self.rs.all_resolutions[f"{res}"]["x"],
                                            "fromY": self.rs.all_resolutions[f"{res}"][
                                                "element_not_present_swipe_y_start"],
                                            "toX": self.rs.all_resolutions[f"{res}"]["x"],
                                            "toY": self.rs.all_resolutions[f"{res}"][
                                                "element_not_present_swipe_y_end"]})
            element_present = self.is_element_present(locator)
            if time.time() > timeout:
                break
