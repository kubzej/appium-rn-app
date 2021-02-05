import names
import os
import json
import random
import string


def PATH(p):
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), p)
    )


def get_list_of_parameters_for_testing(json_file):
    with open(json_file) as file:
        data = json.load(file)
        l = []
        for i in data:
            tuple_of_values = tuple(i.values())
            # tuple_of_values = tuple_of_values[1:]
            l.append(tuple_of_values)
        return l


prefix = ''.join([random.choice(string.ascii_lowercase + string.digits) for n in range(8)])
domain = '@spendee.com'
auttest_prefix = "qa.aut."
email_register = auttest_prefix + prefix + domain
email_login = "automation@spendee.com"
email_not_existing = "automation_not_existing@spendee.com"
password = "spendee123"
password_invalid = "abc"
first_name = names.get_first_name()
last_name = names.get_last_name()


default_set_of_categories = ["Food & Drink", "Shopping", "Transport", "Home", "Bills & Fees", "Entertainment",
                             "Car", "Travel", "Family & Personal", "Healthcare", "Education", "Groceries",
                             "Gifts", "Sport & Hobbies", "Beauty", "Work", "Other", "Salary", "Business", "Gifts",
                             "Extra Income", "Loan", "Parental Leave", "Insurance Payout", "Other"]

accessible_currencies = ["AFN", "ALL"]

calendar_months = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7,
                   "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}

recurrences = ["every day", "every 2 days", "every working day", "every week", "every 2 weeks",
               "every 4 weeks", "every month", "every 2 months", "every 3 months", "every 6 months",
               "every year"]

reminders = ["current day", "1 day in advance", "2 days in advance", "3 days in advance", "4 days in advance",
             "5 days in advance", "6 days on advance", "7 days in advance"]

# APPS
app_android = PATH('../dp-spendee-app/android/app/build/outputs/apk/devel/debug/' + 'app-devel-debug.apk')
# app_ios = PATH('../SpendeeRN/ios/build/Spendee-Devel/Build/Products/Devel.Debug-iphonesimulator/' + 'Spendee.app')
app_ios = PATH('../../../../Library/Developer/Xcode/DerivedData/Spendee-dsjzhbbigatyedfungmtfqinppze/Build/Products/Devel.Debug-iphonesimulator/Spendee.app')

# JSONs FOR TESTS
json_test_create_transaction = r'../../resources/test_parameters/test_create_transaction_parameters.json'
json_test_create_transfer = r'../../resources/test_parameters/test_create_transfer_parameters.json'
json_test_edit_transaction = r'../../resources/test_parameters/test_edit_transaction_parameters.json'
json_test_edit_transfer = r'../../resources/test_parameters/test_edit_transfer_parameters.json'
json_test_change_transfer_to_transaction = r'../../resources/test_parameters/test_change_transfer_to_transaction_parameters.json'
json_test_create_transaction_template = r'../../resources/test_parameters/test_create_transaction_template_parameters.json'
json_test_edit_transaction_template = r'../../resources/test_parameters/test_edit_transaction_template_parameters.json'
json_test_create_transfer_template = r'../../resources/test_parameters/test_create_transfer_template_parameters.json'
json_test_edit_transfer_template = r'../../resources/test_parameters/test_edit_transfer_template_parameters.json'
json_test_generate_transaction_from_template = r'../../resources/test_parameters/test_generate_transaction_from_template_parameters.json'
json_test_generate_transfer_from_template = r'../../resources/test_parameters/test_generate_transfer_from_template_parameters.json'