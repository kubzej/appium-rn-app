import pytest
import pytest_check as check
from selenium.common.exceptions import NoSuchElementException
import time

import variables as vs
import secrets as s
from conftest import PLATFORM
from element_wrapper import ElementWrapper
from page_objects.authentication.authentication_actions import AuthenticationActions
from page_objects.authentication.email_password import EmailPassword
from page_objects.authentication.welcome_screen import WelcomeScreen
from page_objects.more.more_general import MoreGeneral
from page_objects.timeline.timeline_general import TimelineGeneral
from page_objects.timeline.transaction.transaction_actions import TransactionActions
from page_objects.timeline.transaction.transaction_detail import TransactionDetail
from page_objects.timeline.transaction.transaction_validator import TransactionValidator
from page_objects.timeline.transfer.origination_destination_modal import TransferDestinationModal
from page_objects.timeline.transfer.origination_destination_modal import TransferOriginationModal
from page_objects.timeline.transfer.transfer_actions import TransferActions
from page_objects.timeline.transfer.transfer_validator import TransferValidator
from page_objects.more.user_profile import UserProfile
from page_objects.authentication.marketing_dialog import MarketingDialog
from page_objects.timeline.transaction_template.transaction_template_validator import TransactionTemplateValidator
from page_objects.timeline.transfer_template.transfer_template_validator import TransferTemplateValidator
from page_objects.budgets.budget_actions import BudgetActions
from page_objects.budgets.budget_validator import BudgetValidator
from page_objects.wallets.wallets_actions import WalletsActions
from page_objects.wallets.wallet_validator import WalletValidator
from page_objects.more.categories.category_actions import CategoryActions
from page_objects.more.categories.category_validator import CategoryValidator
from page_objects.more.bank_accounts.bank_accounts_actions import BankAccountsActions
from page_objects.more.bank_accounts.bank_accounts_general import BankAccountsGeneral
from page_objects.more.bank_accounts.bank_account_detail import BankAccountDetail
from page_objects.more.subscription.purchase_screen import PurchaseScreen
from page_objects.more.bank_accounts.bank_search_screen import BankSearchScreen
from page_objects.more.advanced.advanced_general import AdvancedGeneral
from page_objects.more.advanced.export.export_actions import ExportActions
from page_objects.wallets.wallet_detail import WalletDetail
from page_objects.budgets.budget_detail import BudgetDetail


@pytest.mark.usefixtures('driver_with_reset')
class TestsWithReset:

    def set_up(self):
        self.ew = ElementWrapper(self.driver)
        self.advanced_general = AdvancedGeneral(self.driver)
        self.authentication_actions = AuthenticationActions(self.driver)
        self.bank_accounts_general = BankAccountsGeneral(self.driver)
        self.bank_search_screen = BankSearchScreen(self.driver)
        self.budget_actions = BudgetActions(self.driver)
        self.budget_detail = BudgetDetail(self.driver)
        self.email_password = EmailPassword(self.driver)
        self.export_actions = ExportActions(self.driver)
        self.marketing_dialog = MarketingDialog(self.driver)
        self.more_general = MoreGeneral(self.driver)
        self.purchase_screen = PurchaseScreen(self.driver)
        self.timeline_general = TimelineGeneral(self.driver)
        self.transactions_actions = TransactionActions(self.driver)
        self.transaction_detail = TransactionDetail(self.driver)
        self.user_profile = UserProfile(self.driver)
        self.wallets_actions = WalletsActions(self.driver)
        self.wallet_detail = WalletDetail(self.driver)
        self.welcome_screen = WelcomeScreen(self.driver)

        self.welcome_screen.skip_notifications_alert()

    @pytest.mark.parametrize("email, password, type_of_test", [
        (s.email_register, s.password, "positive"),
        (s.prefix, s.password, "invalid_email"),
        (s.email_register, s.password_invalid, "invalid password"),
        (s.email_login, s.password, "existing email")
    ])
    def test_register_by_email(self, email, password, type_of_test):
        self.set_up()
        self.authentication_actions.register_by_email(email, password)

        if type_of_test == "positive":
            self.ew.wait_till_element_is_visible(self.user_profile.MORE_ABOUT_YOU_HEADER, 30)
            self.user_profile.set_first_name(vs.first_name)
            self.user_profile.set_last_name(vs.last_name)
            self.ew.tap_element(self.user_profile.CONTINUE_BUTTON)
            self.marketing_dialog.agree_with_marketing()
            try:
                self.ew.wait_till_element_is_visible(self.timeline_general.NAVIGATION_TIMELINE, 30)
            except NoSuchElementException:
                pass
            assert self.ew.is_element_present(self.timeline_general.NAVIGATION_TIMELINE) is True

        elif type_of_test == "existing email":
            try:
                self.ew.wait_till_element_is_visible(self.email_password.EXISTING_EMAIL_DIALOG, 10)
            except NoSuchElementException:
                pass
            assert self.ew.is_element_present(self.email_password.EXISTING_EMAIL_DIALOG) is True
        else:
            assert self.ew.is_element_present(self.email_password.VALIDATION_ERROR_WARNING) is True

    @pytest.mark.parametrize("email, password, type_of_test", [
        (s.email_login, s.password, "positive"),
        (s.email_not_existing, s.password, "existing_email"),
        (s.email_login, s.password_invalid, "invalid_password")
        ])
    def test_login_by_email(self, email, password, type_of_test):
        self.set_up()
        self.authentication_actions.login_by_email(email, password)

        if type_of_test == "positive":
            try:
                self.ew.wait_till_element_is_visible(self.timeline_general.NAVIGATION_TIMELINE, 30)
            except NoSuchElementException:
                pass

            assert self.ew.is_element_present(self.timeline_general.NAVIGATION_TIMELINE) is True
        else:
            try:
                self.ew.wait_till_element_is_visible(self.email_password.INVALID_CREDENTIALS_DIALOG, 10)
            except NoSuchElementException:
                pass
            assert self.ew.is_element_present(self.email_password.INVALID_CREDENTIALS_DIALOG) is True

    def test_logout(self):
        self.set_up()
        self.authentication_actions.login_by_email(s.email_login, s.password)
        self.authentication_actions.logout()

        try:
            self.ew.wait_till_element_is_visible(self.welcome_screen.WELCOME_SCREEN, 10)
        except NoSuchElementException:
            pass
        assert self.ew.is_element_present(self.welcome_screen.WELCOME_SCREEN) is True

    @pytest.mark.parametrize("email, type_of_user", [
        (s.email_free_user, "free"),
        (s.email_plus_user, "plus"),
        (s.email_premium_user, "premium"),
        (s.email_lifetime_user, "lifetime")
    ])
    def test_operations_per_type_of_subscription(self, email, type_of_user):
        self.set_up()
        self.authentication_actions.login_by_email(email, s.password)
        self.ew.wait_till_element_is_visible(self.timeline_general.NAVIGATION_TIMELINE, 30)

        # More Wallets
        self.wallets_actions.create_wallet(name="random", amount=None, currency=None, categories=None)
        self.wallets_actions.save_wallet()
        if type_of_user == "free":
            check.is_true(self.ew.is_element_present(self.purchase_screen.SUBSCRIPTION_HEADER))
        else:
            check.is_false(self.ew.is_element_present(self.purchase_screen.SUBSCRIPTION_HEADER))
        if self.ew.is_element_present(self.purchase_screen.BACK_BUTTON):
            self.ew.tap_element(self.purchase_screen.BACK_BUTTON)
            self.ew.wait_till_element_is_not_visible(self.purchase_screen.SUBSCRIPTION_HEADER, 10)
        if self.ew.is_element_present(self.wallet_detail.WALLET_HEADER):
            self.ew.wait_and_tap_element(self.wallet_detail.BACK_BUTTON, 5)
            self.ew.wait_and_tap_element(self.wallet_detail.DISCARD_CHANGES, 10)

        # More Budgets
        self.budget_actions.create_budget(name="random", amount="random", currency=None, wallets=None, categories=None,
                                          recurrence=None, start_date=None, end_date=None)
        self.budget_actions.save_budget()
        if type_of_user == "free":
            check.is_true(self.ew.is_element_present(self.purchase_screen.SUBSCRIPTION_HEADER))
        else:
            check.is_false(self.ew.is_element_present(self.purchase_screen.SUBSCRIPTION_HEADER))
        if self.ew.is_element_present(self.purchase_screen.BACK_BUTTON):
            self.ew.tap_element(self.purchase_screen.BACK_BUTTON)
            self.ew.wait_till_element_is_not_visible(self.purchase_screen.SUBSCRIPTION_HEADER, 10)
        if self.ew.is_element_present(self.budget_detail.BUDGET_HEADER):
            self.ew.wait_and_tap_element(self.budget_detail.BACK_BUTTON, 5)
            self.ew.wait_and_tap_element(self.budget_detail.DISCARD_CHANGES, 10)

        # Share Wallet
        self.wallets_actions.invite_user_to_wallet()
        if type_of_user == "free":
            check.is_true(self.ew.is_element_present(self.purchase_screen.SUBSCRIPTION_HEADER))
        else:
            check.is_false(self.ew.is_element_present(self.purchase_screen.SUBSCRIPTION_HEADER))
        if self.ew.is_element_present(self.purchase_screen.BACK_BUTTON):
            self.ew.tap_element(self.purchase_screen.BACK_BUTTON)
        if self.ew.is_element_present(self.wallet_detail.DENY_BUTTON):
            self.ew.tap_element(self.wallet_detail.DENY_BUTTON)
            self.ew.wait_and_tap_element(self.wallet_detail.BACK_BUTTON, 10)
        self.ew.wait_till_element_is_visible(self.wallet_detail.WALLET_HEADER, 10)
        self.ew.wait_and_tap_element(self.wallet_detail.BACK_BUTTON, 5)
        self.ew.wait_and_tap_element(self.wallet_detail.DISCARD_CHANGES, 10)

        # More Labels
        self.timeline_general.go_to_timeline()
        self.transactions_actions.open_transaction()
        self.transaction_detail.fast_select_labels(2)
        if type_of_user == "free":
            check.is_true(self.ew.is_element_present(self.transaction_detail.PREMIUM_LABEL_ALERT))
            self.ew.wait_and_tap_element(self.transaction_detail.NOT_NOW_BUTTON, 10)
        else:
            check.is_false(self.ew.is_element_present(self.transaction_detail.PREMIUM_LABEL_ALERT))
        self.ew.wait_and_tap_element(self.transaction_detail.BACK_BUTTON, 10)

        # Connect Bank Account
        self.more_general.go_to_more_section()
        self.more_general.go_to_bank_accounts()
        self.ew.wait_and_tap_element(self.bank_accounts_general.CONNECT_BANK_ACCOUNT_BUTTON, 10)
        self.ew.wait_till_element_is_visible(self.bank_search_screen.SEARCH_INPUT, 30)
        self.bank_search_screen.search_bank_by_search_box("random")
        if type_of_user in ["free", "plus"]:
            check.is_true(self.ew.is_element_present(self.purchase_screen.SUBSCRIPTION_HEADER))
        else:
            check.is_false(self.ew.is_element_present(self.purchase_screen.SUBSCRIPTION_HEADER))
        if self.ew.is_element_present(self.purchase_screen.BACK_BUTTON):
            self.ew.tap_element(self.purchase_screen.BACK_BUTTON)
        self.ew.wait_and_tap_element(self.bank_search_screen.BACK_BUTTON, 10)
        self.ew.wait_and_tap_element(self.bank_accounts_general.BACK_BUTTON, 10)

        # Export Custom Period
        self.more_general.go_to_advanced()
        self.advanced_general.go_to_export()
        self.export_actions.set_period("Custom Period")
        try:
            self.ew.wait_till_element_is_visible(self.export_actions.SELECT_DATE_RANGE_PICKER, 5)
        except NoSuchElementException:
            pass
        if type_of_user == "free":
            check.is_true(self.ew.is_element_present(self.export_actions.PERIOD_SIZE_PICKER))
        else:
            check.is_false(self.ew.is_element_present(self.export_actions.PERIOD_SIZE_PICKER))
        if self.ew.is_element_present(self.export_actions.PERIOD_SIZE_PICKER):
            self.ew.tap_element(self.export_actions.BACKDROP)
        if self.ew.is_element_present(self.export_actions.SELECT_DATE_RANGE_PICKER):
            self.ew.wait_and_tap_element(self.export_actions.BACKDROP, 5)
            self.ew.wait_till_element_is_not_visible(self.export_actions.SELECT_DATE_RANGE_PICKER, 10)

        # Export All Time Period
        self.export_actions.set_period("All Time")
        if type_of_user == "free":
            check.is_true(self.ew.is_element_present(self.export_actions.PERIOD_SIZE_PICKER))
        else:
            check.is_false(self.ew.is_element_present(self.export_actions.PERIOD_SIZE_PICKER))
        if self.ew.is_element_present(self.export_actions.PERIOD_SIZE_PICKER):
            self.ew.tap_element(self.export_actions.BACKDROP)

        # Export XLSX Format
        self.export_actions.set_format("XLSX")
        if type_of_user == "free":
            check.is_false(self.ew.is_element_present(self.export_actions.XLSX_TRUE))
        else:
            check.is_true(self.ew.is_element_present(self.export_actions.XLSX_TRUE))


@pytest.mark.usefixtures('driver_without_reset')
class TestsWithoutReset:

    def set_up(self):
        self.ew = ElementWrapper(self.driver)
        self.bank_accounts_actions = BankAccountsActions(self.driver)
        self.bank_account_detail = BankAccountDetail(self.driver)
        self.bank_accounts_general = BankAccountsGeneral(self.driver)
        self.budget_actions = BudgetActions(self.driver)
        self.budget_validator = BudgetValidator(self.driver)
        self.category_actions = CategoryActions(self.driver)
        self.category_validator = CategoryValidator(self.driver)
        self.more_general = MoreGeneral(self.driver)
        self.transaction_actions = TransactionActions(self.driver)
        self.transaction_detail = TransactionDetail(self.driver)
        self.transaction_validator = TransactionValidator(self.driver)
        self.transaction_template_validator = TransactionTemplateValidator(self.driver)
        self.transfer_actions = TransferActions(self.driver)
        self.transfer_destination_modal = TransferDestinationModal(self.driver)
        self.transfer_origination_modal = TransferOriginationModal(self.driver)
        self.transfer_validator = TransferValidator(self.driver)
        self.transfer_template_validator = TransferTemplateValidator(self.driver)
        self.user_profile = UserProfile(self.driver)
        self.wallets_actions = WalletsActions(self.driver)
        self.wallet_validator = WalletValidator(self.driver)

    def test_edit_profile_name(self):
        self.set_up()

        first_name = vs.first_name
        last_name = vs.last_name

        self.more_general.go_to_more_section()
        self.more_general.go_to_user_profile()
        self.user_profile.clear_first_name()
        self.user_profile.clear_last_name()
        self.user_profile.set_first_name(first_name)
        self.user_profile.set_last_name(last_name)
        self.user_profile.save_user_profile()
        assert self.more_general.get_full_name_on_more_section() == f"{first_name} {last_name}"

    @pytest.mark.parametrize(
        "type_of_test, transaction_type, category, amount, currency, wallet, start_date, note, label, photo, recurrence, end_date, reminder",
        [
            # ("Test", "random", "random", "random", None, None, None, None, None, None, None, None, None)
            i for i in vs.get_list_of_parameters_for_testing(vs.json_test_create_transaction)
        ])
    def test_create_transaction(self, type_of_test, transaction_type, category, amount, currency, wallet, start_date,
                                note, label, photo, recurrence, end_date, reminder):
        self.set_up()
        self.transaction_actions.create_transaction(transaction_type, category, amount, currency, wallet, start_date,
                                                    note, label, photo, recurrence, end_date, reminder)
        attributes = self.transaction_validator.get_all_attributes()
        self.transaction_actions.save_transaction()
        assert self.transaction_validator.is_transaction_on_timeline(attributes) is True

    @pytest.mark.parametrize("type_of_test, amount, outgoing_wallet, incoming_wallet, start_date, note, recurrence, end_date, reminder", [
        # ("Test", "random", None, "oos", None, None, None, None, None)
        i for i in vs.get_list_of_parameters_for_testing(vs.json_test_create_transfer)
    ])
    def test_create_transfer(self, type_of_test, amount, outgoing_wallet, incoming_wallet, start_date, note, recurrence, end_date, reminder):
        self.set_up()
        self.transfer_actions.create_transfer(amount, outgoing_wallet, incoming_wallet, start_date, note, recurrence, end_date, reminder)
        attributes = self.transfer_validator.get_all_attributes()
        self.transaction_actions.save_transaction()
        if self.transfer_origination_modal.is_origination_modal_present() or self.transfer_destination_modal.is_destination_modal_present():
            self.transfer_origination_modal.create_as_new_transaction()
        assert self.transfer_validator.is_transfer_on_timeline(attributes) is True

    @pytest.mark.parametrize(
        "type_of_test, transaction_type, category, amount, wallet, start_date, note, label, photo, recurrence, end_date, reminder",
        [
            # ("Test", None, None, None, None, None, None, None, None, None, None, None)
            i for i in vs.get_list_of_parameters_for_testing(vs.json_test_edit_transaction)
        ])
    def test_edit_transaction(self, type_of_test, transaction_type, category, amount, wallet, start_date, note, label, photo, recurrence, end_date, reminder):
        self.set_up()
        self.transaction_actions.open_transaction()
        self.transaction_actions.edit_transaction(transaction_type, category, amount, wallet, start_date, note, label, photo,  recurrence, end_date, reminder)
        attributes = self.transaction_validator.get_all_attributes()
        self.transaction_actions.save_transaction()
        assert self.transaction_validator.is_transaction_on_timeline(attributes) is True

    def test_change_transaction_to_transfer(self):
        self.set_up()
        self.transaction_actions.open_transaction()
        self.ew.wait_and_tap_element(self.transaction_detail.CATEGORY_ICON, 10)
        self.transaction_detail.set_type_to_transfer()
        attributes = self.transfer_validator.get_all_attributes()
        self.transaction_actions.save_transaction()
        assert self.transfer_validator.is_transfer_on_timeline(attributes)

    @pytest.mark.parametrize(
        "type_of_test, transaction_type, amount, outgoing_wallet, incoming_wallet, start_date, note, recurrence, end_date, reminder",
        [
            # ("Test", None, None, None, None, None, None, None, None, None)
            i for i in vs.get_list_of_parameters_for_testing(vs.json_test_edit_transfer)
        ])
    def test_edit_transfer(self, type_of_test, transaction_type, amount, outgoing_wallet, incoming_wallet, start_date, note, recurrence, end_date, reminder):
        self.set_up()
        self.transfer_actions.open_transfer()
        self.transfer_actions.edit_transfer(transaction_type, amount, outgoing_wallet, incoming_wallet, start_date, note, recurrence, end_date, reminder)
        attributes = self.transfer_validator.get_all_attributes()
        self.transaction_actions.save_transaction()
        assert self.transfer_validator.is_transfer_on_timeline(attributes) is True

    def test_change_1way_transfer_to_2way(self):
        self.set_up()
        self.transfer_actions.create_transfer(amount="random", outgoing_wallet="oos", incoming_wallet="not_oos",
                                              start_date=None, note=None, recurrence=None, end_date=None, reminder=None)
        self.transaction_actions.save_transaction()
        self.transfer_actions.open_transfer()
        self.transaction_detail.set_wallet('not_oos', "transfer_outgoing")
        attributes = self.transfer_validator.get_all_attributes()
        self.transaction_actions.save_transaction()
        assert self.transfer_validator.is_transfer_on_timeline(attributes)

    @pytest.mark.parametrize(
        "type_of_test, outgoing_wallet, incoming_wallet, transaction_type",
        [
            # ("Test", None, None, None)
            i for i in vs.get_list_of_parameters_for_testing(vs.json_test_change_transfer_to_transaction)
        ])
    def test_change_transfer_to_transaction(self, type_of_test, outgoing_wallet, incoming_wallet, transaction_type):
        self.set_up()
        self.transfer_actions.create_transfer(amount="random", outgoing_wallet=outgoing_wallet, incoming_wallet=incoming_wallet, start_date=None, note=None, recurrence=None, end_date=None,  reminder=None)
        self.transaction_actions.save_transaction()
        self.transfer_actions.open_transfer()
        self.transfer_actions.edit_transfer(transaction_type=transaction_type, amount=None, outgoing_wallet=None, incoming_wallet=None, start_date=None, note=None, recurrence=None, end_date=None, reminder=None)
        attributes = self.transaction_validator.get_all_attributes()
        self.transaction_actions.save_transaction()
        assert self.transaction_validator.is_transaction_on_timeline(attributes)

    def test_delete_transaction(self):
        self.set_up()
        self.transaction_actions.open_transaction()
        attributes = self.transaction_validator.get_all_attributes()
        self.transaction_actions.delete_transaction()
        assert self.transaction_validator.is_transaction_on_timeline(attributes) is False

    def test_delete_transfer(self):
        self.set_up()
        self.transfer_actions.open_transfer()
        attributes = self.transfer_validator.get_all_attributes()
        self.transaction_actions.delete_transaction()
        assert self.transfer_validator.is_transfer_on_timeline(attributes) is False

    @pytest.mark.parametrize(
        "type_of_test, transaction_type, category, amount, currency, wallet, start_date, note, label, photo, recurrence, end_date, reminder",
        [
            # ("Test", "random", "random", "random", None, None, None, None, None, None, None, None, None)
            i for i in vs.get_list_of_parameters_for_testing(vs.json_test_create_transaction_template)
        ])
    def test_create_transaction_template(self, type_of_test, transaction_type, category, amount, currency, wallet,
                                          start_date, note, label, photo, recurrence, end_date, reminder):
        self.set_up()
        self.transaction_actions.create_transaction(transaction_type, category, amount, currency, wallet, start_date, note, label,
                                                    photo, recurrence, end_date, reminder)
        attributes = self.transaction_template_validator.get_all_attributes()
        self.transaction_actions.save_transaction()
        assert self.transaction_template_validator.is_transaction_template_on_timeline(attributes)

    @pytest.mark.parametrize(
        "type_of_test, transaction_type, category, amount, wallet, start_date, note, label, photo, recurrence, end_date, reminder",
        [
            # ("Test", None, None, None, None, None, None, None, None, None, None, None)
            i for i in vs.get_list_of_parameters_for_testing(vs.json_test_edit_transaction_template)
        ])
    def test_edit_transaction_template(self, type_of_test, transaction_type, category, amount, wallet,
                                          start_date, note, label, photo, recurrence, end_date, reminder):
        self.set_up()
        self.transaction_actions.open_transaction_template()
        self.transaction_actions.edit_transaction(transaction_type, category, amount, wallet, start_date, note, label, photo, recurrence, end_date, reminder)
        attributes = self.transaction_template_validator.get_all_attributes()
        self.transaction_actions.save_transaction()
        assert self.transaction_template_validator.is_transaction_template_on_timeline(attributes) is True

    def test_change_transaction_template_to_transfer_template(self):
        self.set_up()
        self.transaction_actions.open_transaction_template()
        attributes_transaction = self.transaction_template_validator.get_all_attributes()
        self.ew.wait_and_tap_element(self.transaction_detail.CATEGORY_ICON, 10)
        self.transaction_detail.set_type_to_transfer()
        attributes_transfer = self.transfer_template_validator.get_all_attributes()
        self.transaction_actions.save_transaction()
        assert self.transaction_template_validator.is_transaction_template_on_timeline(attributes_transaction) is False
        assert self.transfer_template_validator.is_transfer_template_on_timeline(attributes_transfer) is True

    @pytest.mark.parametrize(
        "type_of_test, amount, outgoing_wallet, incoming_wallet, start_date, note, recurrence, end_date, reminder", [
            # ("Test", "random", None, None, None, None, "random", None, None)
            i for i in vs.get_list_of_parameters_for_testing(vs.json_test_create_transfer_template)
        ])
    def test_create_transfer_template(self, type_of_test, amount, outgoing_wallet, incoming_wallet, start_date, note, recurrence, end_date, reminder):
        self.set_up()
        self.transfer_actions.create_transfer(amount, outgoing_wallet, incoming_wallet, start_date, note, recurrence, end_date, reminder)
        attributes = self.transfer_template_validator.get_all_attributes()
        self.transaction_actions.save_transaction()
        assert self.transfer_template_validator.is_transfer_template_on_timeline(attributes)

    @pytest.mark.parametrize(
        "type_of_test, transaction_type, amount, outgoing_wallet, incoming_wallet, start_date, note, recurrence, end_date, reminder",
        [
            # ("Test", None, None, None, None, None, None, None, None, "random")
            i for i in vs.get_list_of_parameters_for_testing(vs.json_test_edit_transfer_template)
        ])
    def test_edit_transfer_template(self, type_of_test, transaction_type, amount, outgoing_wallet, incoming_wallet, start_date, note, recurrence, end_date, reminder):
        self.set_up()
        self.transfer_actions.open_transfer_template()
        self.transfer_actions.edit_transfer(transaction_type, amount, outgoing_wallet, incoming_wallet, start_date, note, recurrence, end_date, reminder)
        attributes = self.transfer_template_validator.get_all_attributes()
        self.transaction_actions.save_transaction()
        assert self.transfer_template_validator.is_transfer_template_on_timeline(attributes)

    @pytest.mark.parametrize(
        "type_of_test, amount, outgoing_wallet, incoming_wallet, start_date, note, recurrence, end_date, reminder, transaction_type", [
            # ("Test", "random", None, None, None, None, "random", None, None)
            i for i in vs.get_list_of_parameters_for_testing(vs.json_test_change_transfer_template_to_transaction_template)
        ])
    def test_change_transfer_template_to_transaction_template(self, type_of_test, amount, outgoing_wallet, incoming_wallet, start_date, note, recurrence,
                                              end_date, reminder, transaction_type):
        self.set_up()
        self.transfer_actions.create_transfer(amount, outgoing_wallet, incoming_wallet, start_date, note, recurrence,
                                              end_date, reminder)
        self.transaction_actions.save_transaction()
        self.transfer_actions.open_transfer_template()
        attributes_transfer = self.transfer_template_validator.get_all_attributes()
        self.ew.wait_and_tap_element(self.transaction_detail.CATEGORY_ICON, 10)
        self.transaction_detail.set_type_of_transaction(transaction_type)
        self.transaction_detail.set_category("random")
        attributes_transaction = self.transaction_template_validator.get_all_attributes()
        self.transaction_actions.save_transaction()
        assert self.transfer_template_validator.is_transfer_template_on_timeline(attributes_transfer) is False
        assert self.transaction_template_validator.is_transaction_template_on_timeline(attributes_transaction) is True

    def test_change_1_way_transfer_template_to_2_way(self):
        self.set_up()
        self.transfer_actions.create_transfer(amount="random", outgoing_wallet="oos", incoming_wallet="not_oos",
                                              start_date=None, note=None, recurrence="random", end_date=None, reminder=None)
        self.transaction_actions.save_transaction()
        self.transfer_actions.open_transfer_template()
        attributes_1way = self.transfer_template_validator.get_all_attributes()
        self.transaction_detail.set_wallet("not_oos", "transfer_outgoing")
        attributes_2way = self.transfer_template_validator.get_all_attributes()
        self.transaction_actions.save_transaction()
        assert self.transfer_template_validator.is_transfer_template_on_timeline(attributes_1way) is False
        assert self.transfer_template_validator.is_transfer_template_on_timeline(attributes_2way) is True

    @pytest.mark.parametrize(
        "type_of_test, transaction_type, category, amount, currency, wallet, start_date, note, label, photo, recurrence, end_date, reminder",
        [
            # ("Test", "random", "random", "random", None, None, None, "random", None, None, "random", None, None)
            i for i in vs.get_list_of_parameters_for_testing(vs.json_test_generate_transaction_from_template)
        ])
    def test_generate_transaction_from_template(self, type_of_test, transaction_type, category, amount, currency, wallet, start_date, note, label, photo, recurrence, end_date, reminder):
        self.set_up()
        self.transaction_actions.create_transaction(transaction_type, category, amount, currency, wallet, start_date, note, label, photo, recurrence, end_date, reminder)
        attributes = self.transaction_validator.get_all_attributes()
        self.transaction_actions.save_transaction()

        if start_date == "future":
            assert self.transaction_validator.is_transaction_on_timeline(attributes) is False
        else:
            assert self.transaction_validator.is_transaction_on_timeline(attributes) is True

    @pytest.mark.parametrize(
        "type_of_test, amount, outgoing_wallet, incoming_wallet, start_date, note, recurrence, end_date, reminder", [
            # ("Test", "random", None, None, None, None, "random", None, None)
            i for i in vs.get_list_of_parameters_for_testing(vs.json_test_generate_transfer_from_template)
        ])
    def test_generate_transfer_from_template(self, type_of_test, amount, outgoing_wallet, incoming_wallet, start_date, note, recurrence, end_date, reminder):
        self.set_up()
        self.transfer_actions.create_transfer(amount, outgoing_wallet, incoming_wallet, start_date, note, recurrence, end_date, reminder)
        attributes = self.transfer_validator.get_all_attributes()
        self.transaction_actions.save_transaction()

        if start_date == "future":
            assert self.transfer_validator.is_transfer_on_timeline(attributes) is False
        else:
            assert self.transfer_validator.is_transfer_on_timeline(attributes) is True

    def test_delete_transaction_template(self):
        self.set_up()
        self.transaction_actions.open_transaction_template()
        attributes = self.transaction_template_validator.get_all_attributes()
        self.transaction_actions.delete_transaction()
        assert self.transaction_template_validator.is_transaction_template_on_timeline(attributes) is False

    def test_delete_transfer_template(self):
        self.set_up()
        self.transfer_actions.open_transfer_template()
        attributes = self.transfer_template_validator.get_all_attributes()
        self.transaction_actions.delete_transaction()
        assert self.transfer_template_validator.is_transfer_template_on_timeline(attributes) is False

    @pytest.mark.parametrize(
        "type_of_test, name, amount, currency, wallets, categories, recurrence, start_date, end_date", [
            # ("Test", "random", "random", None, None, None, None, None, None)
            i for i in vs.get_list_of_parameters_for_testing(vs.json_test_create_budget)
        ])
    def test_create_budget(self, type_of_test, name, amount, currency, wallets, categories, recurrence, start_date, end_date):
        self.set_up()
        self.budget_actions.create_budget(name, amount, currency, wallets, categories, recurrence, start_date, end_date)
        attributes = self.budget_validator.get_all_attributes()
        self.budget_actions.save_budget()
        assert self.budget_validator.is_budget_existing(attributes) is True

    @pytest.mark.parametrize(
        "type_of_test, name, amount, currency, wallets, categories, recurrence, start_date, end_date", [
            # ("Test", "random", "random", None, None, None, None, None, None)
            i for i in vs.get_list_of_parameters_for_testing(vs.json_test_edit_budget)
        ])
    def test_edit_budget(self, type_of_test, name, amount, currency, wallets, categories, recurrence, start_date, end_date):
        self.set_up()
        self.budget_actions.edit_budget(name, amount, currency, wallets, categories, recurrence, start_date, end_date)
        attributes = self.budget_validator.get_all_attributes()
        self.budget_actions.save_budget()
        assert self.budget_validator.is_budget_existing(attributes) is True

    def test_delete_budget(self):
        self.set_up()
        self.budget_actions.open_budget()
        attributes = self.budget_validator.get_all_attributes()
        self.budget_actions.delete_budget()
        assert self.budget_validator.is_budget_existing(attributes) is False

    @pytest.mark.parametrize(
        "type_of_test, name, amount, currency, categories", [
            # ("Test", "random", None, None, None)
            i for i in vs.get_list_of_parameters_for_testing(vs.json_test_create_wallet)
        ])
    def test_create_wallet(self, type_of_test, name, amount, currency, categories):
        self.set_up()
        self.wallets_actions.create_wallet(name, amount, currency, categories)
        attributes = self.wallet_validator.get_all_attributes()
        self.wallets_actions.save_wallet()
        assert self.wallet_validator.is_wallet_existing(attributes) is True

    @pytest.mark.parametrize(
        "type_of_test, name, amount, currency, categories", [
        #     ("Test", None, "random", None, None)
            i for i in vs.get_list_of_parameters_for_testing(vs.json_test_edit_wallet)
        ])
    def test_edit_wallet(self, type_of_test, name, amount, currency, categories):
        self.set_up()
        self.wallets_actions.edit_wallet(name, amount, currency, categories)
        attributes = self.wallet_validator.get_all_attributes()
        self.wallets_actions.save_wallet()
        assert self.wallet_validator.is_wallet_existing(attributes)

    def test_delete_wallet(self):
        self.set_up()
        self.wallets_actions.open_wallet()
        attributes = self.wallet_validator.get_all_attributes()
        self.wallets_actions.delete_wallet()
        assert self.wallet_validator.is_wallet_existing(attributes) is False

    def test_create_category(self):
        self.set_up()
        self.more_general.go_to_more_section()
        self.more_general.go_to_categories()
        self.category_actions.create_category(type_of_category="random", name="random", color="random", image="random")
        attributes = self.category_validator.get_all_attributes()
        self.category_actions.save_category()
        assert self.category_validator.is_category_existing(attributes) is True

    def test_edit_category(self):
        self.set_up()
        self.more_general.go_to_more_section()
        self.more_general.go_to_categories()
        self.category_actions.edit_category(type_of_category="random", name="random", color="random", image="random")
        attributes = self.category_validator.get_all_attributes()
        self.category_actions.save_category()
        assert self.category_validator.is_category_existing(attributes) is True

    def test_delete_category(self):
        self.set_up()
        self.more_general.go_to_more_section()
        self.more_general.go_to_categories()
        self.category_actions.open_category()
        attributes = self.category_validator.get_all_attributes()
        self.category_actions.delete_category()
        assert self.category_validator.is_category_existing(attributes) is False

    def test_merge_categories(self):
        self.set_up()
        self.more_general.go_to_more_section()
        self.more_general.go_to_categories()
        self.category_actions.merge_categories()
        remaining, deleted = self.category_validator.get_selected_categories()
        self.category_actions.confirm_merge()
        assert self.category_validator.is_category_existing(remaining)
        assert self.category_validator.is_category_existing(deleted) is False

    def test_connect_bank_account(self):
        self.set_up()
        self.more_general.go_to_more_section()
        self.more_general.go_to_bank_accounts()
        self.bank_accounts_actions.connect_bank_account(vs.fake_bank_simple)
        if PLATFORM == "Android":
            visible_banks = self.ew.get_text_of_elements(self.bank_accounts_actions.bank_accounts_general.BANK_ITEM_NAME)
            assert vs.fake_bank_simple in visible_banks
        else:
            assert self.ew.is_element_present(vs.fake_bank_simple) is True

    def test_bank_account_consent(self):
        self.set_up()
        self.more_general.go_to_more_section()
        self.more_general.go_to_bank_accounts()
        if self.ew.is_element_present(self.bank_accounts_general.BANK_ITEM):
            self.bank_accounts_general.open_bank_account()
        else:
            self.bank_accounts_actions.connect_bank_account(vs.fake_bank_simple)
            self.bank_accounts_general.open_bank_account()
        self.bank_account_detail.open_consent()
        assert self.ew.is_element_present(self.bank_account_detail.CONSENT_WEBVIEW)

    def test_disconnect_bank_account(self):
        self.set_up()
        self.more_general.go_to_more_section()
        self.more_general.go_to_bank_accounts()
        if self.ew.is_element_present(self.bank_accounts_general.BANK_ITEM):
            v_input = len(self.ew.get_elements(self.bank_accounts_general.BANK_ITEM))
            self.bank_accounts_general.open_bank_account()
        else:
            self.bank_accounts_actions.connect_bank_account(vs.fake_bank_simple)
            v_input = len(self.ew.get_elements(self.bank_accounts_general.BANK_ITEM))
            self.bank_accounts_general.open_bank_account()
        self.bank_account_detail.disconnect_bank_account()
        v_output = len(self.ew.get_elements(self.bank_accounts_general.BANK_ITEM))
        assert v_input - v_output == 1

    def test_hide_bank_wallets(self):
        self.set_up()
        self.more_general.go_to_more_section()
        self.more_general.go_to_bank_accounts()
        if self.ew.is_element_present(self.bank_accounts_general.BANK_ITEM):
            self.bank_accounts_general.open_bank_account()
        else:
            self.bank_accounts_actions.connect_bank_account(vs.fake_bank_simple)
            self.bank_accounts_general.open_bank_account()
        number_of_changes = vs.random_number_from_1_to_3
        v_input = len(self.ew.get_elements(self.bank_account_detail.EYE_ICON))
        self.bank_account_detail.hide_bank_wallets(number_of_changes)
        self.ew.wait_and_tap_element(self.bank_account_detail.BACK_BUTTON, 5)
        self.bank_accounts_general.open_bank_account()
        assert v_input - len(self.ew.get_elements(self.bank_account_detail.EYE_ICON)) == number_of_changes







