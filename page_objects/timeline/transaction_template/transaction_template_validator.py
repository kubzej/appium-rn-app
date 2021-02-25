import time

from appium.webdriver.common.touch_action import TouchAction

from conftest import PLATFORM
from element_wrapper import ElementWrapper
from page_objects.timeline.filters.period_filter import PeriodFilter
from page_objects.timeline.timeline_general import TimelineGeneral
from page_objects.timeline.transaction.transaction_detail import TransactionDetail
from page_objects.timeline.transaction.transaction_validator import TransactionValidator
from resolutions import Resolutions


class TransactionTemplateValidator:

    def __init__(self, driver):
        self.driver = driver
        self.action = TouchAction(self.driver)
        self.ew = ElementWrapper(self.driver)
        self.period_filter = PeriodFilter(self.driver)
        self.rs = Resolutions(self.driver)
        self.timeline_general = TimelineGeneral(self.driver)
        self.transaction_detail = TransactionDetail(self.driver)
        self.transaction_validator = TransactionValidator(self.driver)

    def get_all_attributes(self):
        """ Getting all attributes of transaction template
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
                          "recurrence": self.transaction_detail.get_recurrence(),
                          "end_date": self.transaction_detail.get_date("end"),
                          "reminder": self.transaction_detail.get_reminder(),
                          }

        return all_attributes

    def is_transaction_template_on_timeline(self, attributes):
        """ Checking if template is visible inside Scheduled section
        :param attributes: dict
        :return: bool
        """
        transaction_locator = f"regular/" \
                              f"{attributes['category']}/" \
                              f"{self.transaction_validator.adjust_amounts(attributes['amount'], attributes['wallet_amount'])[0]}/" \
                              f"{self.transaction_validator.adjust_amounts(attributes['amount'], attributes['wallet_amount'])[1]}/" \
                              f"{attributes['wallet']}/" \
                              f"undefined/" \
                              f"{self.transaction_validator.adjust_note(attributes['note'])}/" \
                              f"{self.transaction_validator.adjust_labels(attributes['labels'])}/" \
                              f"{str(attributes['photo']).lower()}/" \
                              f"{self.adjust_recurrence(attributes['recurrence'])}/" \
                              f"{self.adjust_end_date(attributes['end_date'])}/" \
                              f"{self.transaction_validator.adjust_reminder(attributes['reminder'])}"

        print(f'LOCATOR: {transaction_locator}')

        self.transaction_validator.prepare_timeline(attributes['start_date'],
                                                    self.adjust_recurrence(attributes['recurrence']))

        android_timeout = time.time() + 60
        ios_timeout = time.time() + 5
        res = self.rs.get_resolution()
        is_transaction_present = self.ew.is_element_present(transaction_locator)

        while is_transaction_present is False:
            if PLATFORM == "Android":
                self.transaction_validator.swipe_android(res)
                is_transaction_present = self.ew.is_element_present(transaction_locator)
                if time.time() > android_timeout:
                    return False
            else:
                is_transaction_present = self.ew.is_element_present(transaction_locator)
                if time.time() > ios_timeout:
                    return False
        return True

    def adjust_recurrence(self, recurrence):
        """ Adjusting recurrence for template locator
        :param recurrence: str
        :return: str
        """
        if recurrence is None or recurrence == "never":
            return "undefined"
        else:
            return recurrence

    def adjust_end_date(self, end_date):
        """ Adjusting end date for template locator
        :param end_date: str
        :return: str
        """
        if end_date is None:
            return "undefined"
        else:
            return end_date
