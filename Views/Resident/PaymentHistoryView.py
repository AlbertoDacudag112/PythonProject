from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView

from Views.Common.StyledWidgets import StyledWidgets


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

        # Apply styling
        StyledWidgets.style_table(self.payment_history_table)

        # Set column resize modes for better layout
        header_widget = self.payment_history_table.horizontalHeader()
        header_widget.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # Payment ID
        header_widget.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Violation ID
        header_widget.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Payment Type
        header_widget.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Amount Paid
        header_widget.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Payment Date
        header_widget.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # Receipt No

        # Enable selection and interaction
        self.payment_history_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.payment_history_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.payment_history_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.payment_history_table.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # Enable sorting
        self.payment_history_table.setSortingEnabled(True)

        # Ensure the table is enabled and accepts mouse events
        self.payment_history_table.setEnabled(True)
        self.payment_history_table.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)

        layout.addWidget(self.payment_history_table)

    def populate_table(self, payments: list):
        """Populate table with payment history"""
        # Disable sorting while populating
        self.payment_history_table.setSortingEnabled(False)

        self.payment_history_table.setRowCount(len(payments))

        for row, payment in enumerate(payments):
            # Payment ID
            id_item = QTableWidgetItem(str(payment.get('PaymentID', '')))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.payment_history_table.setItem(row, 0, id_item)

            # Violation ID
            violation_item = QTableWidgetItem(str(payment.get('ViolationID', '')))
            violation_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            violation_item.setFlags(violation_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.payment_history_table.setItem(row, 1, violation_item)

            # Payment Type
            type_item = QTableWidgetItem(str(payment.get('PaymentType', '')))
            type_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            type_item.setFlags(type_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.payment_history_table.setItem(row, 2, type_item)

            # Amount
            amount_paid = payment.get('AmountPaid', 0)
            try:
                amount_paid = float(amount_paid)
            except (ValueError, TypeError):
                amount_paid = 0.0
            amount_item = QTableWidgetItem(f"₱{amount_paid:.2f}")
            amount_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            amount_item.setFlags(amount_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            # Store numeric value for sorting
            amount_item.setData(Qt.ItemDataRole.UserRole, amount_paid)
            self.payment_history_table.setItem(row, 3, amount_item)

            # Date
            date_item = QTableWidgetItem(str(payment.get('payment_date', '')))
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            date_item.setFlags(date_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.payment_history_table.setItem(row, 4, date_item)

            # Receipt No
            receipt_item = QTableWidgetItem(str(payment.get('ReceiptNo', '')))
            receipt_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            receipt_item.setFlags(receipt_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.payment_history_table.setItem(row, 5, receipt_item)

        # Re-enable sorting after population
        self.payment_history_table.setSortingEnabled(True)

        # Ensure table is visible and enabled after population
        self.payment_history_table.setEnabled(True)
        self.payment_history_table.setVisible(True)