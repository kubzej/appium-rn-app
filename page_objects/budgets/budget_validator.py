import datetime
import time

from appium.webdriver.common.touch_action import TouchAction

import variables as vs
from conftest import PLATFORM
from element_wrapper import ElementWrapper
from page_objects.budgets.budget_detail import BudgetDetail
from page_objects.budgets.budget_overview import BudgetOverview
from page_objects.budgets.budgets_general import BudgetsGeneral
from page_objects.timeline.transaction.transaction_detail import TransactionDetail
from resolutions import Resolutions


class BudgetValidator:

    def __init__(self, driver):
        self.driver = driver
        self.action = TouchAction(self.driver)
        self.budget_detail = BudgetDetail(self.driver)
        self.budgets_general = BudgetsGeneral(self.driver)
        self.budget_overview = BudgetOverview(self.driver)
        self.ew = ElementWrapper(self.driver)
        self.rs = Resolutions(self.driver)
        self.transaction_detail = TransactionDetail(self.driver)

    def get_all_attributes(self):
        """ Getting all attributes of budget
        :return: dict
        """
        all_attributes = {"name": self.budget_detail.get_name(),
                          "amount": self.budget_detail.get_amount(),
                          "currency": self.budget_detail.get_currency(),
                          "wallets": self.budget_detail.get_wallets(),
                          "categories": self.budget_detail.get_categories(),
                          "recurrence": self.budget_detail.get_recurrence(),
                          "start_date": self.transaction_detail.get_date("start"),
                          "end_date": self.transaction_detail.get_date("end")
                          }

        return all_attributes

    def is_budget_existing(self, attributes):
        """ Checking if budget is visible inside Budgets section
        :param attributes: dict
        :return: bool
        """
        budget_locator = f"{attributes['name']}/" \
                         f"{attributes['amount']}/" \
                         f"{attributes['currency']}/" \
                         f"{self.adjust_wallets(attributes['wallets'])}/" \
                         f"{self.adjust_categories(attributes['categories'])}/" \
                         f"{self.adjust_recurrence(attributes['recurrence'])}/" \
                         f"{attributes['start_date']}/" \
                         f"{self.adjust_end_date(attributes['end_date'], attributes['start_date'], attributes['recurrence'])}"

        print(f'ATTRIBUTES: {attributes}')
        print(f'LOCATOR: {budget_locator}')

        if self.ew.is_element_present(self.budget_overview.OVERVIEW_BUTTON):
            self.ew.tap_element(self.budget_overview.BACK_BUTTON)
            self.ew.wait_till_element_is_visible(self.budgets_general.BUDGETS_HEADER, 10)

        android_timeout = time.time() + 30
        ios_timeout = time.time() + 5
        res = self.rs.get_resolution()
        is_budget_present = self.ew.is_element_present(budget_locator)
        while is_budget_present is False:
            if PLATFORM == "Android":
                self.action.long_press(None, self.rs.all_resolutions[f"{res}"]["x"],
                                       self.rs.all_resolutions[f"{res}"]["budget_overview_y_start"]) \
                    .move_to(None, self.rs.all_resolutions[f"{res}"]["x"],
                             self.rs.all_resolutions[f"{res}"]["budget_overview_y_end"]) \
                    .release().perform()
                is_budget_present = self.ew.is_element_present(budget_locator)
                if time.time() > android_timeout:
                    return False
            else:
                is_budget_present = self.ew.is_element_present(budget_locator)
                if time.time() > ios_timeout:
                    return False
        return True

    def adjust_wallets(self, wallets):
        """ Adjusting wallets for budget locator
        :param wallets: str
        :return: str
        """
        if wallets == "All Wallets":
            return "undefined"
        elif wallets in ["0", "2", "3", "4", "5", "6", "7", "8", "9", "10"]:
            return wallets
        else:
            return "1"

    def adjust_categories(self, categories):
        """ Adjusting categories for budget locator
        :param categories: str
        :return: str
        """
        if categories == "All Expenses":
            return "undefined"
        else:
            return categories

    def adjust_recurrence(self, recurrence):
        """ Adjusting recurrence for recurrence locator
        :param recurrence: str
        :return: str
        """
        recurrences_in_app = ["once", "day", "week", "every two weeks", "month", "year"]
        return recurrences_in_app[vs.budget_recurrences.index(recurrence)]

    def adjust_end_date(self, end_date, start_date, recurrence):
        """ Adjusting end date for budget locator
        :param end_date: str
        :param start_date: str
        :param recurrence: str
        :return: str
        """
        if end_date is None:
            year_start, month_start, day_start = (int(x) for x in start_date.split('-'))
            start_date = datetime.date(year_start, month_start, day_start)

            if (year_start % 4) == 0:
                if (year_start % 100) == 0:
                    if (year_start % 400) == 0:
                        is_year_leap = True
                    else:
                        is_year_leap = False
                else:
                    is_year_leap = True
            else:
                is_year_leap = False

            if recurrence == "Daily":
                end_date = start_date
            elif recurrence == "Weekly":
                end_date = str(start_date + datetime.timedelta(days=6))
            elif recurrence == "Biweekly":
                end_date = str(start_date + datetime.timedelta(days=13))
            elif recurrence == "Monthly":
                if month_start in ["01", "03", "05", "07", "08", "10", "12"]:
                    end_date = str(start_date + datetime.timedelta(days=30))
                elif month_start in ["04", "06", "09", "11"]:
                    end_date = str(start_date + datetime.timedelta(days=29))
                else:
                    if is_year_leap:
                        end_date = str(start_date + datetime.timedelta(days=28))
                    else:
                        end_date = str(start_date + datetime.timedelta(days=27))
            elif recurrence == "Yearly":
                if is_year_leap:
                    end_date = str(start_date + datetime.timedelta(days=365))
                else:
                    end_date = str(start_date + datetime.timedelta(days=364))

        return end_date
