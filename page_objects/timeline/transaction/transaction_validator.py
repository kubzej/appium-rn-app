import datetime
import time

from appium.webdriver.common.touch_action import TouchAction

from conftest import PLATFORM
from element_wrapper import ElementWrapper
from page_objects.timeline.filters.period_filter import PeriodFilter
from page_objects.timeline.timeline_general import TimelineGeneral
from page_objects.timeline.transaction.transaction_detail import TransactionDetail
from resolutions import Resolutions


class TransactionValidator:

    def __init__(self, driver):
        self.driver = driver
        self.action = TouchAction(self.driver)
        self.ew = ElementWrapper(self.driver)
        self.period_filter = PeriodFilter(self.driver)
        self.rs = Resolutions(self.driver)
        self.timeline_general = TimelineGeneral(self.driver)
        self.transaction_detail = TransactionDetail(self.driver)

    def get_all_attributes(self):
        """ Getting all attributes of transaction
        :return: dict
        """
        all_attributes = {"category": self.transaction_detail.get_category(),
                          "amount": self.transaction_detail.get_amount(),
                          "wallet_amount": self.transaction_detail.get_wallet_amount(),
                          "currency": self.transaction_detail.get_currency(),
                          "wallet": self.transaction_detail.get_wallet("transaction"),
                          "start_date": self.transaction_detail.get_date("start"),
                          "note": self.transaction_detail.get_note(),
                          "labels": self.transaction_detail.get_labels(True),
                          "photo": self.transaction_detail.get_photo(),
                          "reminder": self.transaction_detail.get_reminder(),
                          }

        return all_attributes

    def is_transaction_on_timeline(self, attributes):
        """ Checking if transaction is visible inside Timeline or Scheduled section
        :param attributes: dict
        :return: bool
        """
        transaction_locator = f"regular/" \
                              f"{attributes['category']}/" \
                              f"{self.adjust_amounts(attributes['amount'], attributes['wallet_amount'])[0]}/" \
                              f"{self.adjust_amounts(attributes['amount'], attributes['wallet_amount'])[1]}/" \
                              f"{attributes['wallet']}/" \
                              f"undefined/" \
                              f"{self.adjust_note(attributes['note'])}/" \
                              f"{self.adjust_labels(attributes['labels'])}/" \
                              f"{str(attributes['photo']).lower()}/" \
                              f"undefined/" \
                              f"undefined/" \
                              f"{self.adjust_reminder(attributes['reminder'])}"

        print(f'LOCATOR: {transaction_locator}')

        self.prepare_timeline(attributes['start_date'], "undefined")

        android_timeout = time.time() + 60
        ios_timeout = time.time() + 5
        res = self.rs.get_resolution()
        is_transaction_present = self.ew.is_element_present(transaction_locator)

        while is_transaction_present is False:
            if PLATFORM == "Android":
                self.swipe_android(res)
                is_transaction_present = self.ew.is_element_present(transaction_locator)
                if time.time() > android_timeout:
                    return False
            else:
                is_transaction_present = self.ew.is_element_present(transaction_locator)
                if time.time() > ios_timeout:
                    return False
        return True

    def adjust_amounts(self, amount, wallet_amount):
        """ Adjusting amount for transaction locator
        :param amount: str
        :param wallet_amount: str
        :return: list of str
        """
        if wallet_amount is None:
            amount_final = amount
            wallet_amount_final = "undefined"
        else:
            amount_final = ""
            for i in wallet_amount:
                if i in ["-", ".", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    amount_final = amount_final + i

            wallet_amount_final = "{:.2f}".format(float(amount))
        return ["{:.2f}".format(float(amount_final)), wallet_amount_final]

    def adjust_note(self, note):
        """ Adjusting note for transaction locator
        :param note: str
        :return: str
        """
        if note is None:
            note = ""
        return note

    def adjust_labels(self, labels):
        """ Adjusting labels for transaction locator
        :param labels: list of str
        :return: list of str
        """
        if len(labels) > 0:
            labels_final = ""
            for i in labels:
                labels_final = labels_final + f",{i}"
            labels_final = labels_final[1:]
        else:
            labels_final = "undefined"

        return labels_final

    def adjust_reminder(self, reminder):
        """ Adjusting reminder for transaction locator
        :param reminder: str
        :return: str
        """
        if reminder is None or reminder == "Never":
            return "undefined"
        else:
            return reminder

    def prepare_timeline(self, start_date, recurrence):
        """ Prepares timeline for transaction search. Opening scheduled screen if transaction has future date.
        :param start_date: str
        :param recurrence: str
        """
        self.ew.wait_till_element_is_visible(self.timeline_general.NAVIGATION_TIMELINE, 30)
        year, month, day = (int(x) for x in start_date.split('-'))
        date = datetime.date(year, month, day)
        today = datetime.date.today()

        if date > today or recurrence != "undefined":

            if self.ew.is_element_present(self.timeline_general.SCHEDULED_SCREEN) is False:
                self.ew.wait_till_element_is_visible(self.timeline_general.TRANSACTION_SECTION, 20)
                self.timeline_general.open_scheduled_section()
            else:
                if PLATFORM == "Android":
                    time.sleep(5)
                else:
                    time.sleep(2)

        elif date < today:
            self.period_filter.set_filter_period(self.period_filter.ALL_TIME_PERIOD)

    def swipe_android(self, resolution):
        """ Looks into past by swiping on android phones
        :param resolution: str
        :return:
        """
        self.action.long_press(None, self.rs.all_resolutions[f"{resolution}"]["x"],
                               self.rs.all_resolutions[f"{resolution}"]["transaction_timeline_up_y_start"]) \
            .move_to(None, self.rs.all_resolutions[f"{resolution}"]["x"],
                     self.rs.all_resolutions[f"{resolution}"]["transaction_timeline_up_y_end"]) \
            .release().perform()
