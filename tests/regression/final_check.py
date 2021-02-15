import pytest
from selenium.common.exceptions import NoSuchElementException

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


@pytest.mark.usefixtures('driver_with_reset')
class TestsWithReset:

    def set_up(self):
        self.ew = ElementWrapper(self.driver)
        self.authentication_actions = AuthenticationActions(self.driver)
        self.email_password = EmailPassword(self.driver)
        self.marketing_dialog = MarketingDialog(self.driver)
        self.timeline_general = TimelineGeneral(self.driver)
        self.user_profile = UserProfile(self.driver)
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


@pytest.mark.usefixtures('driver_without_reset')
class TestsWithoutReset:

    def set_up(self):
        self.ew = ElementWrapper(self.driver)
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




