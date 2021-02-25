import random

from appium.webdriver.common.touch_action import TouchAction

import variables as vs
from conftest import PLATFORM
from element_wrapper import ElementWrapper
from resolutions import Resolutions


class ExportActions:
    BACKDROP = "Backdrop"

    # WALLETS
    WALLETS = "Wallets"

    # PERIOD
    PERIOD = "Period"
    PERIOD_SIZE_PICKER = "Period size Picker"
    SELECT_DATE_RANGE_PICKER = "Select date range Picker"

    # FORMAT
    FORMAT = "Format"
    FORMAT_PICKER = "Format Picker"
    if PLATFORM == "Android":
        XLSX_TRUE = "Excel (.xlsx)-true"
    else:
        XLSX_TRUE = 'label == "Excel (.xlsx)-true"'

    def __init__(self, driver):
        self.driver = driver
        self.action = TouchAction(self.driver)
        self.ew = ElementWrapper(self.driver)
        self.rs = Resolutions(self.driver)

    def set_period(self, period):
        """ Selects period from period picker
        :param period: str
        """

        self.ew.wait_and_tap_element(self.PERIOD, 10)
        self.ew.wait_till_element_is_visible(self.PERIOD_SIZE_PICKER, 10)

        if period == "random":
            period = random.choice(vs.export_periods)

        res = self.rs.get_resolution()
        if PLATFORM == "Android":
            item_visible = self.ew.is_element_present(period)
            while item_visible is False:
                self.action.long_press(None, self.rs.all_resolutions[f"{res}"]["x"],
                                       self.rs.all_resolutions[f"{res}"]["default_picker_up_y_start"]) \
                    .move_to(None, self.rs.all_resolutions[f"{res}"]["x"],
                             self.rs.all_resolutions[f"{res}"]["default_picker_up_y_end"]) \
                    .release().perform()
                item_visible = self.ew.is_element_present(period)
            self.ew.wait_and_tap_element(period, 5)
        else:
            item_visible = self.ew.get_attribute(period, "visible")
            while item_visible == "false":
                self.driver.execute_script("mobile: dragFromToForDuration",
                                           {"duration": "0.1",
                                            "fromX": self.rs.all_resolutions[f"{res}"]["x"],
                                            "fromY": self.rs.all_resolutions[f"{res}"]["default_picker_up_y_start"],
                                            "toX": self.rs.all_resolutions[f"{res}"]["x"],
                                            "toY": self.rs.all_resolutions[f"{res}"]["default_picker_up_y_end"]})
                item_visible = self.ew.get_attribute(period, "visible")
            self.driver.execute_script("mobile: tap", {"x": 100, "y": 50, "element": self.ew.get_element(period)})

    def set_format(self, format):
        """ Selects format of file from format picker
        :param format: str
        """

        self.ew.wait_and_tap_element(self.FORMAT, 10)
        self.ew.wait_till_element_is_visible(self.FORMAT_PICKER, 10)

        if format == "random":
            format = random.choice(vs.export_formats)

        self.ew.wait_and_tap_element(format, 5)
