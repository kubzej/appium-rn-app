import datetime
import random
import string
import time

from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException

import variables as vs
from conftest import PLATFORM
from element_wrapper import ElementWrapper
from resolutions import Resolutions
import validator as vr


class TransactionDetail:

    # OTHER
    BACK_BUTTON = "Back Button"
    if PLATFORM == "Android":
        TRANSACTION_HEADER_TITLE = "Transaction Header Title"
    else:
        TRANSACTION_HEADER_TITLE = '**/XCUIElementTypeStaticText[`label == "Transaction Header Title"`]'
    SAVE_TRANSACTION_BUTTON = "Save Transaction Button"
    TRASH_ICON = "Trash Icon"
    DELETE_BUTTON = "Delete"

    # KEYBOARD
    KEYBOARD = {"0": "Numpad 0", "1": "Numpad 1", "2": "Numpad 2", "3": "Numpad 3", "4": "Numpad 4", "5": "Numpad 5",
                "6": "Numpad 6", "7": "Numpad 7", "8": "Numpad 8", "9": "Numpad 9",
                ".": "Numpad Decimal Point", ",": "Numpad Decimal Point"}
    NUMPAD_BACKDROP = "Numpad Backdrop"
    NUMPAD_CLEAR = "Numpad Clear"

    # TYPE AND CATEGORY
    CATEGORY_ICON = "Category Icon"
    EXPENSES_PICKER = "Expenses Picker"
    INCOME_PICKER = "Income Picker"
    TRANSACTION_PICKER = "Transaction Picker"
    TRANSFER_PICKER = "Transfer Picker"
    if PLATFORM == "Android":
        SELECTED_TYPE = "Selected Type"
    else:
        SELECTED_TYPE = '**/XCUIElementTypeStaticText[`label == "Selected Type"`]'
    GEAR_ICON = "Gear Icon"
    CONFIRM_CATEGORY_ICON = "Confirm Category Icon"

    # AMOUNT
    if PLATFORM == "Android":
        AMOUNT_INPUT = "//android.view.ViewGroup[@content-desc='Amount Input']/android.view.ViewGroup/android.widget.TextView"
        WALLET_AMOUNT = "//android.view.ViewGroup[@content-desc='Wallet Price']/android.widget.TextView"
    else:
        AMOUNT_INPUT = 'label == "Amount Input"'
        WALLET_AMOUNT = "//XCUIElementTypeOther[@name='Wallet Price']/XCUIElementTypeStaticText"

    # CURRENCY
    CONFIRM_BUTTON = "Confirm Button"
    if PLATFORM == "Android":
        CURRENCY = "Currency"
    else:
        CURRENCY = "(//XCUIElementTypeOther[@name='Currency'])[1]/XCUIElementTypeOther"
    SELECTED_CURRENCY_ANDROID = "//android.view.ViewGroup[@content-desc='Currency']/android.widget.TextView"

    # WALLET
    if PLATFORM == "Android":
        WALLET = "Wallet"
        OUTGOING_WALLET = "Outgoing Wallet"
        INCOMING_WALLET = "Incoming Wallet"
        WALLET_ITEM = '//android.view.ViewGroup[@content-desc="Select Wallet Picker"]/android.widget.ScrollView/' \
                      'android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup'
    else:
        WALLET = 'label == "Wallet"'
        OUTGOING_WALLET = 'label == "Outgoing Wallet"'
        INCOMING_WALLET = 'label == "Incoming Wallet"'
        WALLET_ITEM = "Wallet Item"
    WALLET_PICKER = "Select Wallet Picker"

    SELECTED_WALLET_ANDROID = "//android.view.ViewGroup[@content-desc='Wallet']//android.widget.TextView[2]"
    SELECTED_OUTGOING_WALLET_ANDROID = "//android.view.ViewGroup[@content-desc='Outgoing Wallet']//android.widget.TextView[2]"
    SELECTED_INCOMING_WALLET_ANDROID = "//android.view.ViewGroup[@content-desc='Incoming Wallet']//android.widget.TextView[2]"

    # START DATE
    CALENDAR_PICKER = "Select date Picker"
    SELECTED_START_DATE_ANDROID = "//android.view.ViewGroup[@content-desc='Start Date']/android.view.ViewGroup/android.widget.TextView"
    SELECTED_START_DATE_ANDROID_2 = "//android.view.ViewGroup[@content-desc='Start Date']/android.widget.TextView"
    SELECTED_END_DATE_ANDROID = "//android.view.ViewGroup[@content-desc='End Date']/android.view.ViewGroup/android.widget.TextView[2]"
    SELECTED_END_DATE_ANDROID_2 = "//android.view.ViewGroup[@content-desc='End Date']/android.widget.TextView[2]"
    SELECTED_START_DATE_ANDROID_BUDGET = '//android.view.ViewGroup[@content-desc="Start Date"]/android.view.ViewGroup/android.widget.TextView[2]'
    SELECTED_START_DATE_ANDROID_BUDGET_2 = '//android.view.ViewGroup[@content-desc="Start Date"]/android.widget.TextView[2]'
    SELECTED_END_DATE_ANDROID_BUDGET = '//android.view.ViewGroup[@content-desc="End Date"]/android.view.ViewGroup/android.widget.TextView[2]'
    SELECTED_END_DATE_ANDROID_BUDGET_2 = '//android.view.ViewGroup[@content-desc="End Date"]/android.widget.TextView[2]'
    if PLATFORM == "Android":
        START_DATE = "Start Date"
        ACTUAL_MONTH_YEAR = "//android.widget.SeekBar/android.widget.TextView"
    else:
        START_DATE = 'label == "Start Date"'
        ACTUAL_MONTH_YEAR = "(//XCUIElementTypeOther[@name='Select date Picker']//XCUIElementTypeOther[contains(@name,'undefined')])[2]"

    # NOTE
    if PLATFORM == "Android":
        NOTE = "Note"
        EXISTING_NOTE = "Note"
    else:
        NOTE = "//XCUIElementTypeTextView[@name='Note Write a note']"
        EXISTING_NOTE = '**/XCUIElementTypeTextView[`label == "Note"`]'
    SELECTED_NOTE_IOS = "Note"
    NOTE_ELEMENT = "Note Element"

    # LABELS
    LABELS = "Labels"
    LABEL_ITEM = "Label Item"
    if PLATFORM == "Android":
        LABEL_INPUT = "//android.widget.EditText"
    else:
        LABEL_INPUT = "//XCUIElementTypeTextField"
    NON_EXISTING_LABEL = "Non Existing Label"
    VISIBLE_LABELS_ANDROID = "//android.view.ViewGroup[@content-desc='Label Item']/android.widget.TextView"
    VISIBLE_LABELS_IOS = "//XCUIElementTypeOther[@name='Label Item']/XCUIElementTypeOther"
    SELECTED_LABELS_ANDROID = "//android.view.ViewGroup[@content-desc='Check Mark']/android.view.ViewGroup/ancestor::*[1]/following-sibling::*[1]"

    # PHOTO
    PHOTO = "Photo"
    SELECTED_PHOTO = "Selected Photo"
    if PLATFORM == "Android":
        CHOOSE_PHOTO = "//android.widget.TextView[2]"
        PHOTO_FOLDER = "//android.widget.RelativeLayout"
        PHOTO_ITEM = "(//android.support.v7.widget.RecyclerView/android.view.ViewGroup)[1]"
    else:
        CHOOSE_PHOTO = "Choose from Library…"
        PHOTO_FOLDER = "All Photos"
        PHOTO_ITEM = "(//XCUIElementTypeImage)[1]"
    ALLOW_PHOTO_ACCESS_ANDROID = "com.android.packageinstaller:id/permission_allow_button"

    # RECURRENCE
    if PLATFORM == "Android":
        RECURRENCE = "Recurrence"
    else:
        RECURRENCE = 'label == "Recurrence"'
    RECURRENCE_PICKER = "Recurrence Picker"
    SELECTED_RECURRENCE_ANDROID = "//android.view.ViewGroup[@content-desc='Recurrence']/android.view.ViewGroup/android.widget.TextView[2]"
    SELECTED_RECURRENCE_ANDROID_EDIT = '//android.view.ViewGroup[@content-desc="Recurrence"]/android.widget.TextView[2]'

    # END DATE
    if PLATFORM == "Android":
        END_DATE = "End Date"
    else:
        END_DATE = 'label == "End Date"'

    # REMINDER
    if PLATFORM == "Android":
        REMINDER = "Reminder"
    else:
        REMINDER = 'label == "Reminder"'
    REMINDER_PICKER = "Reminder Picker"
    SELECTED_REMINDER_ANDROID = "//android.view.ViewGroup[@content-desc='Reminder']/android.view.ViewGroup/android.widget.TextView[2]"

    def __init__(self, driver):
        self.driver = driver
        self.action = TouchAction(self.driver)
        self.ew = ElementWrapper(self.driver)
        self.rs = Resolutions(self.driver)

    def set_type_of_transaction(self, transaction_type):
        if transaction_type == "random":
            transaction_type = random.choice([self.EXPENSES_PICKER, self.INCOME_PICKER])
        elif transaction_type == "opposite":
            actual_type = self.get_type_of_transaction()
            if actual_type == "Expenses":
                transaction_type = self.INCOME_PICKER
            else:
                transaction_type = self.EXPENSES_PICKER
        elif transaction_type == "expenses":
            transaction_type = self.EXPENSES_PICKER
        elif transaction_type == "income":
            transaction_type = self.INCOME_PICKER

        if transaction_type == self.EXPENSES_PICKER:
            v_input = "Expenses"
        else:
            v_input = "Income"

        self.ew.wait_and_tap_element(transaction_type, 5)
        if PLATFORM == "Android":
            time.sleep(0.5)

        vr.validate_input_against_output(v_input, self.get_type_of_transaction())

    def get_type_of_transaction(self):
        self.ew.wait_till_element_is_visible(self.SELECTED_TYPE, 5)
        if PLATFORM == "Android":
            return self.ew.get_text_of_element(self.SELECTED_TYPE)
        else:
            return self.ew.get_attribute(self.SELECTED_TYPE, "name")

    def set_type_to_transfer(self):
        self.ew.wait_and_tap_element(self.TRANSFER_PICKER, 5)

        self.ew.wait_till_element_is_not_visible(self.TRANSFER_PICKER, 5)
        if self.ew.is_element_present(self.NUMPAD_BACKDROP):
            pass
        else:
            vr.validate_input_against_output("Transfer", self.get_category())

    def open_type_picker(self):
        self.ew.wait_and_tap_element(self.CATEGORY_ICON, 5)

    def set_category(self, category):
        self.ew.wait_till_element_is_visible(self.TRANSACTION_PICKER, 5)
        if category == "random":
            category_visible = False
            timeout = time.time() + 15
            while category_visible is False:
                category = random.choice(vs.default_set_of_categories)
                category_visible = self.ew.is_element_present(f"Category {category}")
                if time.time() > timeout:
                    break

        self.ew.tap_element(f"Category {category}")

        self.ew.wait_till_element_is_not_visible(self.TRANSACTION_PICKER, 5)
        if self.ew.is_element_present(self.NUMPAD_BACKDROP):
            pass
        else:
            vr.validate_input_against_output(category, self.get_category())

    def get_category(self):
        self.ew.wait_till_element_is_visible(self.TRANSACTION_HEADER_TITLE, 5)
        if PLATFORM == "Android":
            category = self.ew.get_text_of_element(self.TRANSACTION_HEADER_TITLE).split(" ")[1:]
        else:
            category = self.ew.get_attribute(self.TRANSACTION_HEADER_TITLE, "name").split(" ")[1:]
        return ' '.join(category)

    def set_amount(self, amount):
        if amount == "random":
            amount = str(random.randint(1, 99))

        self.ew.wait_till_element_is_visible(self.KEYBOARD["1"], 10)
        amount_list = list(amount)
        for i in amount_list:
            self.ew.wait_and_tap_element(self.KEYBOARD[i], 5)
        self.ew.wait_and_tap_element(self.NUMPAD_BACKDROP, 5)

        v_output = self.get_amount()
        if v_output.startswith("-"):
            v_output = v_output[1:]
        vr.validate_input_against_output(''.join(str(i) for i in amount_list), v_output)

    def get_amount(self):
        self.ew.wait_till_element_is_visible(self.AMOUNT_INPUT, 5)
        if PLATFORM == "Android":
            return self.ew.get_text_of_element(self.AMOUNT_INPUT)
        else:
            amount = self.ew.get_attribute(self.AMOUNT_INPUT, "name")
            if amount.startswith("+"):
                amount = amount[1:]
            return amount

    def get_wallet_amount(self):
        self.ew.wait_till_element_is_visible(self.AMOUNT_INPUT, 5)
        try:
            if PLATFORM == "Android":
                return self.ew.get_text_of_element(self.WALLET_AMOUNT)
            else:
                return self.ew.get_attribute(self.WALLET_AMOUNT, "name")
        except NoSuchElementException:
            return None

    def set_currency(self, currency):
        if currency == "random":
            currency = random.choice(vs.accessible_currencies)
        self.ew.wait_and_tap_element(self.CURRENCY, 5)
        self.ew.wait_and_tap_element(f"Currency {currency}", 10)
        self.set_exchange_rate()

        vr.validate_input_against_output(currency, self.get_currency())

    def get_currency(self):
        self.ew.wait_till_element_is_visible(self.CURRENCY, 5)
        if PLATFORM == "Android":
            return self.ew.get_attribute(self.SELECTED_CURRENCY_ANDROID, "content-desc")
        else:
            return self.ew.get_attribute(self.CURRENCY, "name")

    def set_exchange_rate(self):
        self.ew.wait_and_tap_element(self.CONFIRM_BUTTON, 10)

    def set_wallet(self, wallet, type_of_wallet):
        selected_wallet = self.get_wallet(type_of_wallet)
        if type_of_wallet == "transaction":
            self.ew.wait_and_tap_element(self.WALLET, 5)
        elif type_of_wallet == "transfer_outgoing":
            self.ew.wait_and_tap_element(self.OUTGOING_WALLET, 5)
        elif type_of_wallet == "transfer_incoming":
            self.ew.wait_and_tap_element(self.INCOMING_WALLET, 5)

        self.ew.wait_till_element_is_visible(self.WALLET_PICKER, 5)
        wallets_in_picker = self.get_wallets_in_picker()

        if wallet == "random":
            wallet = random.choice(wallets_in_picker)
            if PLATFORM == "Android":
                self.ew.tap_element(wallet)
            else:
                self.ew.tap_element(f'label == "{wallet}"')
        elif wallet == "different":
            wallets_in_picker.remove(selected_wallet)
            wallet = random.choice(wallets_in_picker)
            if PLATFORM == "Android":
                self.ew.tap_element(wallet)
            else:
                self.ew.tap_element(f'label == "{wallet}"')
        elif wallet == "oos":

            for i in wallets_in_picker:
                if i.startswith('Out of Spendee'):
                    postfix_oos = i.split('-')[1]

            wallet = f"Out of Spendee-{postfix_oos}"
            if PLATFORM == "Android":
                self.ew.tap_element(wallet)
            else:
                self.ew.tap_element(f'label == "{wallet}"')
        elif wallet == "not_oos":
            if self.ew.is_element_present("Out of Spendee-false"):
                wallets_in_picker.remove("Out of Spendee-false")
            elif self.ew.is_element_present("Out of Spendee-true"):
                wallets_in_picker.remove("Out of Spendee-true")
            wallet = random.choice(wallets_in_picker)
            if PLATFORM == "Android":
                self.ew.tap_element(wallet)
            else:
                self.ew.tap_element(f'label == "{wallet}"')
        else:
            if PLATFORM == "Android":
                self.ew.tap_element(wallet)
            else:
                self.ew.tap_element(f'label == "{wallet}"')

        self.ew.wait_till_element_is_not_visible(self.WALLET_PICKER, 5)
        if self.ew.is_element_present(self.CONFIRM_BUTTON):
            self.set_exchange_rate()

        v_input = wallet.split('-')[0]
        vr.validate_input_against_output(v_input, self.get_wallet(type_of_wallet))

    def get_wallet(self, type_of_wallet):

        if PLATFORM == "Android":
            if type_of_wallet == "transaction":
                self.ew.wait_till_element_is_visible(self.SELECTED_WALLET_ANDROID, 5)
                return self.ew.get_text_of_element(self.SELECTED_WALLET_ANDROID)
            elif type_of_wallet == "transfer_outgoing":
                self.ew.wait_till_element_is_visible(self.SELECTED_OUTGOING_WALLET_ANDROID, 5)
                return self.ew.get_text_of_element(self.SELECTED_OUTGOING_WALLET_ANDROID)
            elif type_of_wallet == "transfer_incoming":
                self.ew.wait_till_element_is_visible(self.SELECTED_INCOMING_WALLET_ANDROID, 5)
                return self.ew.get_text_of_element(self.SELECTED_INCOMING_WALLET_ANDROID)
        else:
            if type_of_wallet == "transaction":
                self.ew.wait_till_element_is_visible(self.WALLET, 5)
                return self.ew.get_attribute(self.WALLET, "name")
            elif type_of_wallet == "transfer_outgoing":
                self.ew.wait_till_element_is_visible(self.OUTGOING_WALLET, 5)
                return self.ew.get_attribute(self.OUTGOING_WALLET, "name")
            elif type_of_wallet == "transfer_incoming":
                self.ew.wait_till_element_is_visible(self.INCOMING_WALLET, 5)
                return self.ew.get_attribute(self.INCOMING_WALLET, "name")

    def get_wallets_in_picker(self):
        if PLATFORM == "Android":
            return self.ew.get_attributes(self.WALLET_ITEM, "content-desc")
        else:
            return self.ew.get_attributes(self.WALLET_ITEM, "label")

    def set_start_date(self, start_date):
        if start_date == "random":
            start_date = str(
                datetime.date(int(datetime.date.today().year), random.randint(1, 12), random.randint(1, 28)))
        elif start_date == "past":
            start_date = str(datetime.date.today() - datetime.timedelta(days=random.randint(1, 30)))
        elif start_date == "future":
            start_date = str(datetime.date.today() + datetime.timedelta(days=random.randint(1, 30)))
        elif start_date == "today":
            start_date = str(datetime.date.today())
        elif start_date == "yesterday":
            start_date = str(datetime.date.today() - datetime.timedelta(days=1))
        elif start_date == "tomorrow":
            start_date = str(datetime.date.today() + datetime.timedelta(days=1))

        self.ew.wait_and_tap_element(self.START_DATE, 5)
        self.ew.wait_till_element_is_visible(self.CALENDAR_PICKER, 5)
        self.set_calendar_month_year(start_date)
        self.set_calendar_day(start_date)

        vr.validate_input_against_output(start_date, self.get_date("start"))

    def set_calendar_month_year(self, date):
        year, month, day = (int(x) for x in date.split('-'))
        if PLATFORM == "Android":
            month_in_app = vs.calendar_months[self.ew.get_text_of_element(self.ACTUAL_MONTH_YEAR).split(" ")[0]]
            year_in_app = int(self.ew.get_text_of_element(self.ACTUAL_MONTH_YEAR).split(" ")[1])
        else:
            month_in_app = vs.calendar_months[self.ew.get_attribute(self.ACTUAL_MONTH_YEAR, "label").split(" ")[0]]
            year_in_app = int(self.ew.get_attribute(self.ACTUAL_MONTH_YEAR, "label").split(" ")[1])

        direction = None
        if (year > year_in_app) or (year == year_in_app and month > month_in_app):
            direction = "up"
        elif (year < year_in_app) or (year == year_in_app and month < month_in_app):
            direction = "down"

        iterations = abs((year - year_in_app) * 12 + (month - month_in_app))
        res = self.rs.get_resolution()

        if PLATFORM == "Android":
            if direction == "up":
                for i in range(iterations):
                    self.action.long_press(None, self.rs.all_resolutions[f"{res}"]["x"],
                                           self.rs.all_resolutions[f"{res}"]["calendar_picker_up_y_start"]) \
                        .move_to(None, self.rs.all_resolutions[f"{res}"]["x"],
                                 self.rs.all_resolutions[f"{res}"]["calendar_picker_up_y_end"]) \
                        .release().perform()
            elif direction == "down":
                for i in range(iterations):
                    for d in range(2):
                        self.action.long_press(None, self.rs.all_resolutions[f"{res}"]["x"],
                                               self.rs.all_resolutions[f"{res}"]["calendar_picker_down_y_start"]) \
                            .move_to(None, self.rs.all_resolutions[f"{res}"]["x"],
                                     self.rs.all_resolutions[f"{res}"]["calendar_picker_down_y_end"]) \
                            .release().perform()
        elif PLATFORM == "iOS":
            if direction == "up":
                for i in range(iterations):
                    self.driver.execute_script("mobile: dragFromToForDuration",
                                               {"duration": "0.1",
                                                "fromX": self.rs.all_resolutions[f"{res}"]["x"],
                                                "fromY": self.rs.all_resolutions[f"{res}"][
                                                    "calendar_picker_up_y_start"],
                                                "toX": self.rs.all_resolutions[f"{res}"]["x"],
                                                "toY": self.rs.all_resolutions[f"{res}"]["calendar_picker_up_y_end"]})
            elif direction == "down":
                for i in range(iterations):
                    self.driver.execute_script("mobile: dragFromToForDuration",
                                               {"duration": "0.1",
                                                "fromX": self.rs.all_resolutions[f"{res}"]["x"],
                                                "fromY": self.rs.all_resolutions[f"{res}"][
                                                    "calendar_picker_down_y_start"],
                                                "toX": self.rs.all_resolutions[f"{res}"]["x"],
                                                "toY": self.rs.all_resolutions[f"{res}"]["calendar_picker_down_y_end"]})

    def set_calendar_day(self, date):
        if PLATFORM == "Android":
            year, month, day = (int(x) for x in date.split('-'))
            if date == str(datetime.date.today()):
                self.ew.tap_element(
                    f"today {datetime.date(year, month, day).strftime('%A')} {datetime.date(year, month, day).strftime('%B')} {day} selected You have no entries for this day ")
            else:
                self.ew.tap_element(
                    f" {datetime.date(year, month, day).strftime('%A')} {datetime.date(year, month, day).strftime('%B')} {day} ")

        elif PLATFORM == "iOS":
            self.ew.wait_and_tap_element(f"native.calendar.SELECT_DATE_SLOT-{date}", 10)

    def get_date(self, type_of_date):
        is_transaction = self.ew.is_element_present(self.TRANSACTION_HEADER_TITLE)
        if type_of_date == "start":
            date_ios = self.START_DATE
            if is_transaction:
                date_android = self.SELECTED_START_DATE_ANDROID
            else:
                date_android = self.SELECTED_START_DATE_ANDROID_BUDGET
        else:
            date_ios = self.END_DATE
            if is_transaction:
                date_android = self.SELECTED_END_DATE_ANDROID
            else:
                date_android = self.SELECTED_END_DATE_ANDROID_BUDGET
        try:
            if PLATFORM == "Android":
                try:
                    self.ew.wait_till_element_is_visible(date_android, 5)
                except NoSuchElementException:
                    if type_of_date == "start":
                        if is_transaction:
                            date_android = self.SELECTED_START_DATE_ANDROID_2
                        else:
                            date_android = self.SELECTED_START_DATE_ANDROID_BUDGET_2
                    else:
                        if is_transaction:
                            date_android = self.SELECTED_END_DATE_ANDROID_2
                        else:
                            date_android = self.SELECTED_END_DATE_ANDROID_BUDGET_2
                date_in_app = self.ew.get_text_of_element(date_android)
            else:
                self.ew.wait_till_element_is_visible(date_ios, 5)
                date_in_app = self.ew.get_attribute(date_ios, "name")
        except (NoSuchElementException, AttributeError):
            return None

        if date_in_app == "Today" or date_in_app == "Yesterday?":
            date = str(datetime.date.today())
        elif date_in_app == "Yesterday":
            date = str(datetime.date.today() - datetime.timedelta(days=1))
        elif date_in_app == "Tomorrow":
            date = str(datetime.date.today() + datetime.timedelta(days=1))
        elif date_in_app is None or date_in_app == "Never":
            return None
        else:
            try:
                month, day, year = (str(x) for x in date_in_app.split(' '))
                day = day.replace(",", "")
            except ValueError:
                month, day = (str(x) for x in date_in_app.split(' '))
                year = str(datetime.date.today().year)
            month = str(datetime.datetime.strptime(month, "%B").month).zfill(2)
            date = f"{year}-{month}-{day.zfill(2)}"

        return date

    def set_note(self, note):
        if note == "random":
            note = ''.join([random.choice(string.ascii_lowercase + string.digits) for n in range(0, 8)])
        self.ew.wait_till_element_is_visible(self.NOTE_ELEMENT, 5)
        self.ew.get_element(self.NOTE).send_keys(note)
        if self.driver.is_keyboard_shown():
            self.ew.tap_element(self.NOTE_ELEMENT)

        vr.validate_input_against_output(note, self.get_note())

    def get_note(self):
        try:
            if PLATFORM == "Android":
                note = self.ew.get_text_of_element(self.NOTE)
                if note == "Write a note":
                    note = ""
                return note
            else:
                return self.ew.get_text_of_elements(self.SELECTED_NOTE_IOS)[2]
        except IndexError:
            return None

    def set_label(self, label):
        self.ew.wait_till_element_is_visible(self.LABELS, 5)
        if label == "random":
            if self.ew.is_element_present(self.LABEL_ITEM):
                labels = self.get_labels(False)
                label = random.choice(labels)
                if PLATFORM == "Android":
                    self.ew.tap_element(label)
                    time.sleep(0.5)
                else:
                    i = labels.index(label)
                    self.action.tap(self.ew.get_elements(self.LABEL_ITEM)[i]).perform()
                vr.validate_input_against_more_outputs(label, self.get_labels(True))
            else:
                self.create_label(label)
        else:
            if PLATFORM == "Android":
                if self.ew.is_element_present(label):
                    self.ew.tap_element(label)
                    time.sleep(0.5)
                    vr.validate_input_against_more_outputs(label, self.get_labels(True))
                else:
                    self.create_label(label)
            else:
                labels = self.get_labels(False)
                if label in labels:
                    i = labels.index(label)
                    self.action.tap(self.ew.get_elements(self.LABEL_ITEM)[i]).perform()
                    vr.validate_input_against_more_outputs(label, self.get_labels(True))
                else:
                    self.create_label(label)

    def create_label(self, name):
        if name == "random":
            name = ''.join([random.choice(string.ascii_lowercase + string.digits) for n in range(0, 8)])

        self.ew.tap_element(self.LABELS)
        self.ew.wait_and_tap_element(self.LABEL_INPUT, 5)
        self.ew.get_element(self.LABEL_INPUT).send_keys(name)
        self.ew.wait_and_tap_element(self.NON_EXISTING_LABEL, 5)
        self.ew.tap_element(self.BACK_BUTTON)

        vr.validate_input_against_more_outputs(name, self.get_labels(True))

    def get_labels(self, only_selected):
        self.ew.wait_till_element_is_visible(self.LABELS, 5)
        if PLATFORM == "Android":
            if only_selected:
                labels = self.ew.get_text_of_elements(self.SELECTED_LABELS_ANDROID)
            else:
                labels = self.ew.get_text_of_elements(self.VISIBLE_LABELS_ANDROID)
        else:
            attributes = self.ew.get_attributes(self.VISIBLE_LABELS_IOS, "name")
            labels = []
            for i in attributes:
                if only_selected:
                    if i.endswith("false") is False:
                        labels.append(i.split("-")[0])
                else:
                    labels.append(i.split("-")[0])

        return labels

    def set_photo(self):
        self.ew.wait_and_tap_element(self.PHOTO, 5)
        self.ew.wait_and_tap_element(self.CHOOSE_PHOTO, 5)
        if self.ew.is_element_present(self.ALLOW_PHOTO_ACCESS_ANDROID):
            self.ew.tap_element(self.ALLOW_PHOTO_ACCESS_ANDROID)
        if PLATFORM == "Android":
            self.ew.wait_and_tap_element(self.PHOTO_FOLDER, 5)
        self.ew.wait_and_tap_element(self.PHOTO_ITEM, 5)

        vr.validate_input_against_output(True, self.get_photo())

    def get_photo(self):
        try:
            self.ew.wait_till_element_is_visible(self.PHOTO, 5)
            self.ew.wait_till_element_is_visible(self.SELECTED_PHOTO, 3)
        except:
            NoSuchElementException()
        return self.ew.is_element_present(self.SELECTED_PHOTO)

    def set_recurrence(self, recurrence):
        if recurrence == "random":
            recurrence = random.choice(vs.recurrences)

        self.ew.wait_and_tap_element(self.RECURRENCE, 5)
        self.ew.wait_till_element_is_visible(self.RECURRENCE_PICKER, 5)

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
        try:
            self.ew.wait_till_element_is_visible(self.RECURRENCE, 5)
            if PLATFORM == "Android":
                try:
                    recurrence = self.ew.get_text_of_element(self.SELECTED_RECURRENCE_ANDROID).lower()
                except AttributeError:
                    recurrence = self.ew.get_text_of_element(self.SELECTED_RECURRENCE_ANDROID_EDIT).lower()
            else:
                recurrence = self.ew.get_attribute(self.RECURRENCE, "name").lower()

            if recurrence != "never" and PLATFORM == "Android":
                recurrences_in_app = ["every day", "every 2 days", "every work day", "every week", "every 2 weeks",
                                      "every 4 weeks", "every month", "every 2 months", "every 3 months", "every 6 months", "every year"]
                recurrence = vs.recurrences[recurrences_in_app.index(recurrence)]
            return recurrence
        except (AttributeError, NoSuchElementException):
            return None

    def set_end_date(self, end_date):
        start_date = self.get_date("start")
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
        self.set_calendar_month_year(end_date)
        self.set_calendar_day(end_date)

        vr.validate_input_against_output(end_date, self.get_date("end"))

    def set_reminder(self, reminder):
        if reminder == "random":
            reminder = random.choice(vs.reminders)

        self.ew.wait_and_tap_element(self.REMINDER, 5)
        self.ew.wait_till_element_is_visible(self.REMINDER_PICKER, 5)

        res = self.rs.get_resolution()
        if PLATFORM == "Android":
            item_visible = self.ew.is_element_present(reminder)
            while item_visible is False:
                self.action.long_press(None, self.rs.all_resolutions[f"{res}"]["x"],
                                       self.rs.all_resolutions[f"{res}"]["default_picker_up_y_start"]) \
                    .move_to(None, self.rs.all_resolutions[f"{res}"]["x"],
                             self.rs.all_resolutions[f"{res}"]["default_picker_up_y_end"]) \
                    .release().perform()
                item_visible = self.ew.is_element_present(reminder)
            self.ew.wait_and_tap_element(reminder, 5)
        else:
            item_visible = self.ew.get_attribute(reminder, "visible")
            while item_visible == "false":
                self.driver.execute_script("mobile: dragFromToForDuration",
                                           {"duration": "0.1",
                                            "fromX": self.rs.all_resolutions[f"{res}"]["x"],
                                            "fromY": self.rs.all_resolutions[f"{res}"]["default_picker_up_y_start"],
                                            "toX": self.rs.all_resolutions[f"{res}"]["x"],
                                            "toY": self.rs.all_resolutions[f"{res}"]["default_picker_up_y_end"]})
                item_visible = self.ew.get_attribute(reminder, "visible")
            self.driver.execute_script("mobile: tap", {"x": 100, "y": 50, "element": self.ew.get_element(reminder)})

        vr.validate_input_against_output(reminder, self.get_reminder())

    def get_reminder(self):
        try:
            self.ew.wait_till_element_is_visible(self.REMINDER, 5)
            if PLATFORM == "Android":
                reminder = self.ew.get_text_of_element(self.SELECTED_REMINDER_ANDROID)
            else:
                reminder = self.ew.get_attribute(self.REMINDER, "name")

            if reminder != "Never":
                reminders_in_app = ["On a transaction date", "1 day before", "2 days before", "3 days before",
                                    "4 days before",
                                    "5 days before", "6 days before", "7 days before"]
                reminder = vs.reminders[reminders_in_app.index(reminder)]
            return reminder
        except (ValueError, NoSuchElementException):
            return None
