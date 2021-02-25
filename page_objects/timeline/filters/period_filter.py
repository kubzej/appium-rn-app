import time

from conftest import PLATFORM
from element_wrapper import ElementWrapper


class PeriodFilter:
    if PLATFORM == "Android":
        PERIOD_FILTER_BUTTON = "Period Filter Button"
    else:
        PERIOD_FILTER_BUTTON = 'label == "Period Filter Button"'

    # PERIODS
    WEEK_PERIOD = "Week"
    MONTH_PERIOD = "Month"
    YEAR_PERIOD = "Year"
    ALL_TIME_PERIOD = "All Time"

    def __init__(self, driver):
        self.driver = driver
        self.ew = ElementWrapper(self.driver)

    def open_period_filter(self):
        self.ew.wait_and_tap_element(self.PERIOD_FILTER_BUTTON, 20)

    def set_filter_period(self, period):
        self.open_period_filter()
        self.ew.wait_till_element_is_visible(period, 10)
        if PLATFORM == "Android":
            self.ew.tap_element(period)
        else:
            self.driver.execute_script("mobile: tap", {"x": 100, "y": 50, "element": self.ew.get_element(period)})

        periods = {self.WEEK_PERIOD: "By weeks", self.MONTH_PERIOD: "By months", self.YEAR_PERIOD: "By years",
                   self.ALL_TIME_PERIOD: "All time"}
        if PLATFORM == "Android":
            self.ew.wait_till_element_is_visible(periods[period], 10)
        else:
            actual_period = self.ew.get_attribute(self.PERIOD_FILTER_BUTTON, "name")
            while actual_period != periods[period]:
                time.sleep(0.5)
                actual_period = self.ew.get_attribute(self.PERIOD_FILTER_BUTTON, "name")
