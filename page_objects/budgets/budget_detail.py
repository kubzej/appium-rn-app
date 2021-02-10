from element_wrapper import ElementWrapper
from conftest import PLATFORM
import string
import random
import time
import validator as vr
import variables as vs
from resolutions import Resolutions
from appium.webdriver.common.touch_action import TouchAction
import datetime
from page_objects.timeline.transaction.transaction_detail import TransactionDetail


class BudgetDetail():

    # OTHER
    BUDGET_HEADER = "Budget Header"
    SAVE_BUDGET_BUTTON = "Save Budget Button"
    TRASH_ICON = "Trash Icon"
    DELETE_BUTTON = "Delete"

    # NAME
    NAME_INPUT = "Name Input"
    SELECTED_NAME_IOS = '**/XCUIElementTypeTextField[`label == "Name Input"`]'

    # AMOUNT
    if PLATFORM == "Android":
        AMOUNT_INPUT = "Amount Input"
    else:
        AMOUNT_INPUT = '**/XCUIElementTypeOther[`label == "Amount Input"`][2]'
    SELECTED_AMOUNT = "Currency Input"

    # KEYBOARD
    KEYBOARD = {"0": "Numpad 0", "1": "Numpad 1", "2": "Numpad 2", "3": "Numpad 3", "4": "Numpad 4", "5": "Numpad 5",
                "6": "Numpad 6", "7": "Numpad 7", "8": "Numpad 8", "9": "Numpad 9",
                ".": "Numpad Decimal Point", ",": "Numpad Decimal Point"}
    NUMPAD_BACKDROP = "Numpad Backdrop"
    NUMPAD_CLEAR = "Numpad Clear"

    # CURRENCY
    CURRENCY = "Currency"

    # WALLETS
    if PLATFORM == "Android":
        WALLET_ITEM = '//android.view.ViewGroup[@content-desc="Select Wallets Picker"]/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup'
        WALLETS = "Wallets"
    else:
        WALLET_ITEM = "Wallet Item"
        WALLETS = 'label == "Wallets"'
    WALLET_PICKER = "Select Wallets Picker"
    SELECTED_WALLETS_ANDROID = '//android.view.ViewGroup[@content-desc="Wallets"]/android.view.ViewGroup/android.widget.TextView[2]'
    SELECTED_WALLETS_ANDROID_2 = '//android.view.ViewGroup[@content-desc="Wallets"]/android.widget.TextView[2]'

    if PLATFORM == "Android":
        SELECTED_CURRENCY = '//android.view.ViewGroup[@content-desc="Currency"]/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText'
        CURRENCY_PICKER = "Select currency Picker"
    else:
        SELECTED_CURRENCY = '**/XCUIElementTypeOther[`label == "Currency"`][1]'
        CURRENCY_PICKER = 'label == "Select currency"'

    # CATEGORIES
    CATEGORIES = "Categories"
    HEADER_BUDGET_FOR = "Header Budget For"
    SELECT_ALL_CHECKED = "Select All-checked"
    SELECT_ALL_UNCHECKED = "Select All-unchecked"
    SELECT_ALL_PART = "Select All-part"
    if PLATFORM == "Android":
        CATEGORIES = "Categories"
        CATEGORY_ITEM = '//android.view.ViewGroup[@content-desc="Category Item"]/android.view.ViewGroup'
        SELECTED_CATEGORIES_ANDROID = '//android.view.ViewGroup[@content-desc="Categories"]/android.widget.TextView[2]'
        SELECTED_CATEGORIES_ANDROID_2 = '//android.view.ViewGroup[@content-desc="Categories"]/android.view.ViewGroup/android.widget.TextView[2]'
    else:
        CATEGORY_ITEM = 'label == "Category Item"'
        CATEGORIES = 'label == "Categories"'
    BACK_BUTTON = "Back Button"

    # RECURRENCE
    if PLATFORM == "Android":
        RECURRENCE = "Recurrence"
        SELECTED_RECURRENCE_ANDROID = '//android.view.ViewGroup[@content-desc="Recurrence"]/android.widget.TextView[2]'
        SELECTED_RECURRENCE_ANDROID_EDIT = '//android.view.ViewGroup[@content-desc="Recurrence"]/android.view.ViewGroup/android.widget.TextView[2]'
    else:
        RECURRENCE = 'label == "Recurrence"'
    RECURRENCE_PICKER = "Recurrence Picker"

    # START DATE
    if PLATFORM == "Android":
        START_DATE = "Start Date"
    else:
        START_DATE = 'label == "Start Date"'
    CALENDAR_PICKER = "Select date Picker"

    # END DATE
    if PLATFORM == "Android":
        END_DATE = "End Date"
    else:
        END_DATE = 'label == "End Date"'

    def __init__(self, driver):
        self.driver = driver
        self.action = TouchAction(self.driver)
        self.ew = ElementWrapper(self.driver)
        self.rs = Resolutions(self.driver)
        self.transaction_detail = TransactionDetail(self.driver)

    def set_name(self, name):
        if name == "random":
            name = ''.join([random.choice(string.ascii_lowercase + string.digits) for n in range(0, 8)])

        self.ew.wait_till_element_is_visible(self.NAME_INPUT, 5)
        self.ew.get_element(self.NAME_INPUT).send_keys(name)

        vr.validate_input_against_output(name, self.get_name())

    def get_name(self):
        self.ew.wait_till_element_is_visible(self.NAME_INPUT, 5)

        if PLATFORM == "Android":
            return self.ew.get_text_of_element(self.NAME_INPUT)
        else:
            return self.ew.get_text_of_element(self.SELECTED_NAME_IOS)

    def set_amount(self, amount):
        if amount == "random":
            amount = str(random.randint(1, 99))

        self.ew.wait_and_tap_element(self.AMOUNT_INPUT, 5)
        self.ew.wait_till_element_is_visible(self.KEYBOARD["1"], 10)
        amount_list = list(amount)
        for i in amount_list:
            self.ew.wait_and_tap_element(self.KEYBOARD[i], 5)
        self.ew.wait_and_tap_element(self.NUMPAD_BACKDROP, 5)

        vr.validate_input_against_output(amount, self.get_amount())

    def get_amount(self):
        self.ew.wait_till_element_is_visible(self.AMOUNT_INPUT, 5)
        if PLATFORM == "Android":
            return self.ew.get_text_of_element(self.SELECTED_AMOUNT)
        else:
            return self.ew.get_attribute(self.AMOUNT_INPUT, "name")

    def set_currency(self, currency):
        if currency == "random":
            currency = random.choice(vs.accessible_currencies)

        self.ew.wait_and_tap_element(self.CURRENCY, 5)
        self.ew.wait_till_element_is_visible(self.CURRENCY_PICKER, 10)
        self.ew.wait_and_tap_element(f"Currency {currency}", 10)
        self.ew.wait_till_element_is_not_visible(self.CURRENCY_PICKER, 10)
        vr.validate_input_against_output(currency, self.get_currency())

    def get_currency(self):
        self.ew.wait_till_element_is_visible(self.CURRENCY, 5)
        if PLATFORM == "Android":
            return self.ew.get_text_of_element(self.SELECTED_CURRENCY)
        else:
            return self.ew.get_attribute(self.SELECTED_CURRENCY, "name")

    def set_wallets(self, wallets):

        self.ew.wait_and_tap_element(self.WALLETS, 5)
        self.ew.wait_till_element_is_visible(self.WALLET_PICKER, 5)

        all_visible_wallets = self.count_wallets()[0]
        selected_wallets = self.count_wallets()[1]
        non_selected_wallets = self.count_wallets()[2]
        total_wallets = len(all_visible_wallets)
        total_selected_wallets = len(selected_wallets)
        total_non_selected_wallets = len(non_selected_wallets)

        if wallets == "random":
            wallets_to_select = random.sample(all_visible_wallets, random.randrange(0, len(all_visible_wallets)))
            for i in wallets_to_select:
                if PLATFORM == "Android":
                    self.ew.tap_element(i)
                else:
                    self.ew.tap_element(f'label == "{i}"')
        elif wallets == "all_selected":
            if total_wallets != total_selected_wallets:
                for i in non_selected_wallets:
                    if PLATFORM == "Android":
                        self.ew.tap_element(i)
                    else:
                        self.ew.tap_element(f'label == "{i}"')
        elif wallets == "all_unselected":
            if total_wallets != total_non_selected_wallets:
                for i in selected_wallets:
                    if PLATFORM == "Android":
                        self.ew.tap_element(i)
                    else:
                        self.ew.tap_element(f'label == "{i}"')
        elif isinstance(wallets, int):
            x = 0
            actual_selected_wallets = self.count_wallets()[1]
            for i in all_visible_wallets:
                x = x + 1
                if x <= wallets and len(actual_selected_wallets) > 1:
                    if PLATFORM == "Android":
                        self.ew.tap_element(i)
                    else:
                        self.ew.tap_element(f'label == "{i}"')
                    actual_selected_wallets = self.count_wallets()[1]

        selected_wallets = self.count_wallets()[1]
        total_wallets = len(self.count_wallets()[0])
        total_selected_wallets = len(selected_wallets)

        if total_wallets == total_selected_wallets:
            v_input = "All Wallets"
        elif total_selected_wallets == 1:
            v_input = selected_wallets[0].split('-')[0]
        else:
            v_input = str(total_selected_wallets)

        self.ew.tap_element('Backdrop')
        vr.validate_input_against_output(v_input, self.get_wallets())

    def count_wallets(self):
        if PLATFORM == "Android":
            all_visible_wallets = self.ew.get_attributes(self.WALLET_ITEM, "content-desc")
        else:
            all_visible_wallets = self.ew.get_attributes(self.WALLET_ITEM, "label")

        selected_wallets = []
        non_selected_wallets = []
        for i in all_visible_wallets:
            if i.endswith('true'):
                selected_wallets.append(i)
            else:
                non_selected_wallets.append(i)
        return (all_visible_wallets, selected_wallets, non_selected_wallets)

    def get_wallets(self):
        self.ew.wait_till_element_is_visible(self.WALLETS, 5)

        if PLATFORM == "Android":
            result = self.ew.get_text_of_element(self.SELECTED_WALLETS_ANDROID)
            if result is None:
                result = self.ew.get_text_of_element(self.SELECTED_WALLETS_ANDROID_2)
        else:
            result = self.ew.get_attribute(self.WALLETS, "name")
        return result

    def set_categories(self, categories):

        self.ew.wait_and_tap_element(self.CATEGORIES, 5)
        self.ew.wait_till_element_is_visible(self.HEADER_BUDGET_FOR, 5)

        all_visible_categories = self.count_categories()[0]

        if categories == "random":
            categories = random.randrange(0, len(all_visible_categories))

        if categories == "all_selected":
            if self.ew.is_element_present(self.SELECT_ALL_UNCHECKED):
                self.ew.tap_element(self.SELECT_ALL_UNCHECKED)
            elif self.ew.is_element_present(self.SELECT_ALL_PART):
                self.ew.tap_element(self.SELECT_ALL_PART)
                self.ew.tap_element(self.SELECT_ALL_UNCHECKED)
        elif categories == "all_unselected":
            if self.ew.is_element_present(self.SELECT_ALL_CHECKED):
                self.ew.tap_element(self.SELECT_ALL_CHECKED)
            elif self.ew.is_element_present(self.SELECT_ALL_PART):
                self.ew.tap_element(self.SELECT_ALL_PART)
        elif isinstance(categories, int):
            if self.ew.is_element_present(self.SELECT_ALL_CHECKED):
                self.ew.tap_element(self.SELECT_ALL_CHECKED)
            elif self.ew.is_element_present(self.SELECT_ALL_PART):
                self.ew.tap_element(self.SELECT_ALL_PART)
            x = 0
            all_visible_categories = self.count_categories()[0]
            for i in all_visible_categories:
                x = x + 1
                if x <= categories:
                    self.ew.tap_element(i)

        if self.ew.is_element_present(self.SELECT_ALL_CHECKED):
            v_input = "All Expenses"
        else:
            v_input = str(len(self.count_categories()[1]))

        self.ew.tap_element(self.BACK_BUTTON)
        vr.validate_input_against_output(v_input, self.get_categories())

    def count_categories(self):
        if PLATFORM == "Android":
            all_visible_categories = self.ew.get_attributes(self.CATEGORY_ITEM, "content-desc")
        else:
            all_items = self.ew.get_attributes(self.CATEGORY_ITEM, "name")
            all_visible_categories = []
            for i in all_items:
                if i != "Category Item":
                    all_visible_categories.append(i)

        selected_categories = []
        non_selected_categories = []
        for i in all_visible_categories:
            if i.endswith('true'):
                selected_categories.append(i)
            else:
                non_selected_categories.append(i)
        return (all_visible_categories, selected_categories, non_selected_categories)

    def get_categories(self):
        self.ew.wait_till_element_is_visible(self.CATEGORIES, 5)

        if PLATFORM == "Android":

            result = self.ew.get_text_of_element(self.SELECTED_CATEGORIES_ANDROID)
            if result is None:
                result = self.ew.get_text_of_element(self.SELECTED_CATEGORIES_ANDROID_2)
            return result
        else:
            return self.ew.get_attribute(self.CATEGORIES, "name")

    def set_recurrence(self, recurrence):
        self.ew.wait_and_tap_element(self.RECURRENCE, 5)
        self.ew.wait_till_element_is_visible(self.RECURRENCE_PICKER, 5)

        if recurrence == "random":
            recurrence = random.choice(vs.budget_recurrences)

        res = self.rs.get_resolution()
        if PLATFORM == "Android":
            item_visible = self.ew.is_element_present(recurrence)
            while item_visible is False:
                self.action.long_press(None, self.rs.all_resolutions[f"{res}"]["x"],
                                       self.rs.all_resolutions[f"{res}"]["default_picker_up_y_start"]) \
                    .move_to(None, self.rs.all_resolutions[f"{res}"]["x"],
                             self.rs.all_resolutions[f"{res}"]["default_picker_up_y_end"]) \
                    .release().perform()
                item_visible = self.ew.is_element_present(recurrence)
            self.ew.wait_and_tap_element(recurrence, 5)
        else:
            item_visible = self.ew.get_attribute(recurrence, "visible")
            while item_visible == "false":
                self.driver.execute_script("mobile: dragFromToForDuration",
                                           {"duration": "0.1",
                                            "fromX": self.rs.all_resolutions[f"{res}"]["x"],
                                            "fromY": self.rs.all_resolutions[f"{res}"]["default_picker_up_y_start"],
                                            "toX": self.rs.all_resolutions[f"{res}"]["x"],
                                            "toY": self.rs.all_resolutions[f"{res}"]["default_picker_up_y_end"]})
                item_visible = self.ew.get_attribute(recurrence, "visible")
            self.driver.execute_script("mobile: tap", {"x": 100, "y": 50, "element": self.ew.get_element(recurrence)})

        vr.validate_input_against_output(recurrence, self.get_recurrence())

    def get_recurrence(self):
        self.ew.wait_till_element_is_visible(self.RECURRENCE, 5)
        if PLATFORM == "Android":
            recurrence = self.ew.get_text_of_element(self.SELECTED_RECURRENCE_ANDROID)
            if recurrence is None:
                recurrence = self.ew.get_text_of_element(self.SELECTED_RECURRENCE_ANDROID_EDIT)
        else:
            recurrence = self.ew.get_attribute(self.RECURRENCE, "name")
        return recurrence

    def set_start_date(self, start_date):
        if start_date == "random":
            start_date = str(
                datetime.date(int(datetime.date.today().year), random.randint(1, 12), random.randint(1, 28)))
        elif start_date == "future":
            start_date = str(datetime.date.today() + datetime.timedelta(days=random.randint(1, 5)))
        elif start_date == "today":
            start_date = str(datetime.date.today())
        elif start_date == "yesterday":
            start_date = str(datetime.date.today() - datetime.timedelta(days=1))
        elif start_date == "tomorrow":
            start_date = str(datetime.date.today() + datetime.timedelta(days=1))

        self.ew.wait_and_tap_element(self.START_DATE, 5)
        self.ew.wait_till_element_is_visible(self.CALENDAR_PICKER, 5)
        self.transaction_detail.set_calendar_month_year(start_date)
        self.transaction_detail.set_calendar_day(start_date)
        vr.validate_input_against_output(start_date, self.transaction_detail.get_date("start"))

    def set_end_date(self, end_date):
        start_date = self.transaction_detail.get_date("start")
        year_start, month_start, day_start = (int(x) for x in start_date.split('-'))
        start_date = datetime.date(year_start, month_start, day_start)

        if end_date == "random":
            end_date = str(start_date + datetime.timedelta(days=random.randint(1, 30)))
        elif end_date == "day_after_start_date":
            end_date = str(start_date + datetime.timedelta(days=1))
        else:
            year_end, month_end, day_end = (int(x) for x in end_date.split('-'))
            end_date = datetime.date(year_end, month_end, day_end)
            if start_date < end_date:
                end_date = str(end_date)
            else:
                raise ValueError(f"endDate {end_date} is not older than start_date {str(start_date)}")

        self.ew.wait_and_tap_element(self.END_DATE, 5)
        self.ew.wait_till_element_is_visible(self.CALENDAR_PICKER, 5)
        self.transaction_detail.set_calendar_month_year(end_date)
        self.transaction_detail.set_calendar_day(end_date)

        vr.validate_input_against_output(end_date, self.transaction_detail.get_date("end"))