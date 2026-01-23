from Models.Database import Database
from Models.PaymentModel import PaymentModel
from Controllers.Utility.ValidationHelper import ValidationHelper


class PaymentController:
    """Handles payment processing business logic"""

    def __init__(self):
        self.db = Database(host='localhost', database='RoadEyeDB', user='root', password='')
        self.payment_model = PaymentModel(self.db)

    def validate_payment_form(self, form_data: dict) -> tuple:
        """
        Validate payment form data

        Returns:
            tuple: (is_valid: bool, error_message: str)
        """
        errors = ValidationHelper.validate_payment_form(form_data)

        if errors:
            return False, "\n".join(errors)

        return True, ""

    def process_payment(self, violation_data: dict, form_data: dict):
        """
        Process payment for a violation

        Args:
            violation_data: Dictionary with violation information
            form_data: Dictionary with payment form data
                       (payer_name, contact, payment_type, reference)

        Returns:
            tuple: (success: bool, result_or_error: dict/str)
        """
        # Validate form
        is_valid, error_msg = self.validate_payment_form(form_data)
        if not is_valid:
            return False, error_msg

        # Process payment
        success, result = self.payment_model.save_payment(
            violation_id=violation_data['violation_id'],
            payment_type=form_data['payment_type'],
            amount=violation_data['fine_amount'],
            payer_name=form_data['payer_name'],
            contact=form_data['contact'],
            reference=form_data.get('reference')
        )

        if success:
            return True, result  # result is payment data dict
        else:
            return False, result  # result is error message