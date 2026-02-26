from Models.Database import Database
from Models.ViolationModel import ViolationModel
from Models.PaymentModel import PaymentModel


class ResidentController:
    """Handles resident dashboard business logic"""

    def __init__(self, user_data: dict):
        self.user_data = user_data
        self.db = Database(host='localhost', database='RoadEyeDB', user='root', password='')
        self.violation_model = ViolationModel(self.db)
        self.payment_model = PaymentModel(self.db)

    def get_dashboard_stats(self):
        """Get statistics for resident dashboard"""
        resident_id = self.user_data['ResidentID']

        total, unpaid = self.violation_model.get_violation_statistics(resident_id)

        return {
            'total_violations': total,
            'unpaid_violations': unpaid,
            'paid_violations': total - unpaid
        }

    def get_monthly_chart_data(self):
        """Get monthly violations data for chart"""
        resident_id = self.user_data['ResidentID']
        return self.violation_model.get_monthly_violations(resident_id)

    def get_violations(self):
        """Get all violations for resident"""
        resident_id = self.user_data['ResidentID']
        return self.violation_model.get_user_violations(resident_id)

    def get_payment_history(self):
        """Get payment history for resident"""
        resident_id = self.user_data['ResidentID']
        return self.payment_model.get_payment_history(resident_id)

    def filter_violations(self, violations: list, search_text: str, status_filter: str):
        """
        Filter violations based on search and status

        Args:
            violations: List of all violations
            search_text: Search query
            status_filter: Status filter ("All", "Paid", "Unpaid")

        Returns:
            Filtered list of violations
        """
        filtered = []
        search_lower = search_text.lower()

        for violation in violations:
            # Status filter
            if status_filter != "All" and violation['status'] != status_filter:
                continue

            # Search filter
            if search_text:
                if (search_lower not in violation['violation_id'].lower() and
                        search_lower not in violation['plate_no'].lower() and
                        search_lower not in violation['violation_type'].lower()):
                    continue

            filtered.append(violation)

        return filtered