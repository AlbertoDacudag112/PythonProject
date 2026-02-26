"""
Utility/ValidationHelper.py
Input validation utilities
"""
import re


class ValidationHelper:
    """Helper class for form validation"""

    @staticmethod
    def validate_username(username: str) -> tuple:
        """
        Validate username input
        Returns: (is_valid: bool, error_message: str)
        """
        username = username.strip()

        if len(username) == 0:
            return False, ""
        elif len(username) < 4:
            return False, "⚠ Username must be at least 4 characters"
        elif not re.match("^[a-zA-Z0-9_]+$", username):
            return False, "⚠ Username can only contain letters, numbers, and underscores"

        return True, ""

    @staticmethod
    def validate_password(password: str) -> tuple:
        """
        Validate password input
        Returns: (is_valid: bool, error_message: str)
        """
        if len(password) == 0:
            return False, ""
        elif len(password) < 6:
            return False, "⚠ Password must be at least 6 characters"

        return True, ""

    @staticmethod
    def validate_confirm_password(password: str, confirm: str) -> tuple:
        """
        Validate confirm password matches password
        Returns: (is_valid: bool, error_message: str)
        """
        if len(confirm) == 0:
            return False, ""
        elif password != confirm:
            return False, "⚠ Passwords do not match"

        return True, ""

    @staticmethod
    def validate_name(name: str, field_name: str = "Name") -> tuple:
        """
        Validate name input (first name, last name)
        Returns: (is_valid: bool, error_message: str)
        """
        name = name.strip()

        if len(name) == 0:
            return False, ""
        elif len(name) < 2:
            return False, f"⚠ {field_name} must be at least 2 characters"
        elif not re.match("^[a-zA-Z ]+$", name):
            return False, f"⚠ {field_name} can only contain letters"

        return True, ""

    @staticmethod
    def validate_contact_number(contact: str) -> tuple:
        """
        Validate Philippine contact number (11 digits starting with 09)
        Returns: (is_valid: bool, error_message: str)
        """
        contact = contact.strip()

        if len(contact) == 0:
            return False, ""
        elif not re.match(r"^[0-9+\-() ]+$", contact):
            return False, "⚠ Invalid contact number format"
        elif len(contact) < 10:
            return False, "⚠ Contact number must be at least 10 digits"

        return True, ""

    @staticmethod
    def validate_contact_number_strict(contact: str) -> tuple:
        """
        Strict validation for Philippine mobile numbers (exactly 11 digits, starts with 09)
        Returns: (is_valid: bool, error_message: str)
        """
        contact = contact.strip()

        if len(contact) == 0:
            return False, "Contact number is required"
        elif len(contact) != 11:
            return False, "Contact number must be exactly 11 digits"
        elif not contact.startswith('09'):
            return False, "Contact number must start with '09'"
        elif not contact.isdigit():
            return False, "Contact number must contain only digits"

        return True, ""

    @staticmethod
    def validate_required_field(value: str, field_name: str = "Field") -> tuple:
        """
        Validate that a field is not empty
        Returns: (is_valid: bool, error_message: str)
        """
        if not value or not value.strip():
            return False, f"{field_name} is required"

        return True, ""

    @staticmethod
    def validate_plate_number(plate_no: str) -> tuple:
        """
        Validate vehicle plate number
        Returns: (is_valid: bool, error_message: str)
        """
        plate_no = plate_no.strip()

        if len(plate_no) == 0:
            return False, "Plate number is required"
        elif len(plate_no) < 3:
            return False, "Plate number is too short"

        return True, ""

    @staticmethod
    def validate_registration_form(form_data: dict) -> list:
        """
        Validate entire registration form
        Returns: list of error messages (empty if valid)
        """
        errors = []

        # Username validation
        is_valid, error = ValidationHelper.validate_username(form_data.get('username', ''))
        if error:
            errors.append(error)

        # Password validation
        is_valid, error = ValidationHelper.validate_password(form_data.get('password', ''))
        if error:
            errors.append(error)

        # Confirm password validation
        is_valid, error = ValidationHelper.validate_confirm_password(
            form_data.get('password', ''),
            form_data.get('confirm_password', '')
        )
        if error:
            errors.append(error)

        # First name validation
        is_valid, error = ValidationHelper.validate_name(
            form_data.get('first_name', ''),
            "First name"
        )
        if error:
            errors.append(error)

        # Last name validation
        is_valid, error = ValidationHelper.validate_name(
            form_data.get('last_name', ''),
            "Last name"
        )
        if error:
            errors.append(error)

        # Contact number validation
        is_valid, error = ValidationHelper.validate_contact_number(
            form_data.get('contact_no', '')
        )
        if error:
            errors.append(error)

        return errors

    @staticmethod
    def validate_payment_form(form_data: dict) -> list:
        """
        Validate payment form
        Returns: list of error messages (empty if valid)
        """
        errors = []

        # Payer name validation
        if not form_data.get('payer_name', '').strip():
            errors.append("Payer name is required")

        # Contact validation
        is_valid, error = ValidationHelper.validate_contact_number_strict(
            form_data.get('contact', '')
        )
        if error:
            errors.append(error)

        # Reference number validation for online payments
        payment_type = form_data.get('payment_type', '')
        online_methods = ["GCash", "PayMaya", "Bank Transfer", "Credit Card", "Debit Card"]

        if payment_type in online_methods:
            if not form_data.get('reference', '').strip():
                errors.append(f"{payment_type} reference number is required")

        return errors