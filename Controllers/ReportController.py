from Models.Database import Database
from Models.ReportModel import ReportModel
from Models.PaymentModel import PaymentModel
from Controllers.Utility.PDFGenerator import PDFGenerator


class ReportController:
    """Handles report generation business logic"""

    def __init__(self):
        self.db = Database(host='localhost', database='RoadEyeDB', user='root', password='')
        self.report_model = ReportModel(self.db)
        self.payment_model = PaymentModel(self.db)

    def get_violations_report_data(self):
        """
        Get all violations data for report

        Returns:
            list: List of violation dictionaries
        """
        return self.report_model.get_violations_report_data()

    def export_violations_report_to_pdf(self, file_path: str, violations_data: list):
        """
        Export violations report to PDF

        Args:
            file_path: Path where PDF will be saved
            violations_data: List of violation dictionaries

        Returns:
            tuple: (success: bool, message: str)
        """
        if not violations_data:
            return False, "No data to export"

        return PDFGenerator.generate_violations_report(file_path, violations_data)

    def get_payment_report_data(self):
        """
        Get payment report data and statistics

        Returns:
            tuple: (statistics_dict, recent_payments_list)
        """
        # Get statistics
        stats = self.report_model.get_payment_report_statistics()

        # Get recent payments
        recent_payments = self.payment_model.get_all_payment_history(limit=10)

        return stats, recent_payments

    def calculate_report_statistics(self, violations: list):
        """
        Calculate statistics from violations data

        Args:
            violations: List of violation dictionaries

        Returns:
            dict: Statistics dictionary
        """
        total = len(violations)
        paid = sum(1 for v in violations if v.get('PaymentStatus') == 'PAID')
        unpaid = total - paid
        total_fines = sum(float(v.get('FineAmount', 0)) for v in violations if v.get('PaymentStatus') == 'PAID')

        return {
            'total': total,
            'paid': paid,
            'unpaid': unpaid,
            'total_revenue': total_fines
        }