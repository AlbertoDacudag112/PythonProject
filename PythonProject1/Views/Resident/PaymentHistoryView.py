from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem

from Views.Common import StyledWidgets


class PaymentHistoryView(QWidget):
    """Payment history table view"""

    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Header
        header = QLabel("Payment History")
        header.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        header.setStyleSheet("color: #e8bb41;")
        layout.addWidget(header)

        # Payment history table
        self.payment_history_table = QTableWidget()
        self.payment_history_table.setColumnCount(6)
        self.payment_history_table.setHorizontalHeaderLabels([
            "Payment ID", "Violation ID", "Payment Type",
            "Amount Paid", "Payment Date", "Receipt No"
        ])

        StyledWidgets.style_table(self.payment_history_table)

        layout.addWidget(self.payment_history_table)

    def populate_table(self, payments: list):
        """Populate table with payment history"""
        self.payment_history_table.setRowCount(len(payments))

        for row, payment in enumerate(payments):
            # Payment ID
            id_item = QTableWidgetItem(payment['PaymentID'])
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.payment_history_table.setItem(row, 0, id_item)

            # Violation ID
            violation_item = QTableWidgetItem(payment['ViolationID'])
            violation_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.payment_history_table.setItem(row, 1, violation_item)

            # Payment Type
            type_item = QTableWidgetItem(payment['PaymentType'])
            type_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.payment_history_table.setItem(row, 2, type_item)

            # Amount
            amount_item = QTableWidgetItem(f"₱{payment['AmountPaid']:.2f}")
            amount_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.payment_history_table.setItem(row, 3, amount_item)

            # Date
            date_item = QTableWidgetItem(payment['payment_date'])
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.payment_history_table.setItem(row, 4, date_item)

            # Receipt No
            receipt_item = QTableWidgetItem(payment['ReceiptNo'])
            receipt_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.payment_history_table.setItem(row, 5, receipt_item)