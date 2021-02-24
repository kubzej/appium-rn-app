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

random_number_from_1_to_3 = random.randint(1, 3)
random_string = ''.join([random.choice(string.ascii_lowercase + string.digits) for n in range(8)])

first_name = names.get_first_name()
last_name = names.get_last_name()

fake_bank_simple = "Fake Bank Simple"

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
budget_recurrences = ["Custom (Once)", "Daily", "Weekly", "Biweekly", "Monthly", "Yearly"]

reminders = ["current day", "1 day in advance", "2 days in advance", "3 days in advance", "4 days in advance",
             "5 days in advance", "6 days on advance", "7 days in advance"]

export_periods = ["Custom Period", "All Time", "Last 30 days", "Last 90 days", "Last 365 days"]

export_formats = ["XLSX", "CSV"]

accessible_colors = ['#f5534b', '#b55a42', '#b47b55', '#d35e00', '#de8135', '#df8c29', '#b9965e', '#ffa200']



# JSONs FOR TESTS
json_test_create_transaction = r'../../resources/test_parameters/test_create_transaction_parameters.json'
json_test_create_transfer = r'../../resources/test_parameters/test_create_transfer_parameters.json'
json_test_edit_transaction = r'../../resources/test_parameters/test_edit_transaction_parameters.json'
json_test_edit_transfer = r'../../resources/test_parameters/test_edit_transfer_parameters.json'
json_test_change_transfer_to_transaction = r'../../resources/test_parameters/test_change_transfer_to_transaction_parameters.json'
json_test_create_transaction_template = r'../../resources/test_parameters/test_create_transaction_template_parameters.json'
json_test_edit_transaction_template = r'../../resources/test_parameters/test_edit_transaction_template_parameters.json'
json_test_create_transfer_template = r'../../resources/test_parameters/test_create_transfer_template_parameters.json'
json_test_change_transfer_template_to_transaction_template = r'../../resources/test_parameters/test_change_transfer_template_to_transaction_template_parameters.json'
json_test_edit_transfer_template = r'../../resources/test_parameters/test_edit_transfer_template_parameters.json'
json_test_generate_transaction_from_template = r'../../resources/test_parameters/test_generate_transaction_from_template_parameters.json'
json_test_generate_transfer_from_template = r'../../resources/test_parameters/test_generate_transfer_from_template_parameters.json'
json_test_create_budget = r'../../resources/test_parameters/test_create_budget_parameters.json'
json_test_edit_budget = r'../../resources/test_parameters/test_edit_budget_parameters.json'
json_test_create_wallet = r'../../resources/test_parameters/test_create_wallet_parameters.json'
json_test_edit_wallet = r'../../resources/test_parameters/test_edit_wallet_parameters.json'