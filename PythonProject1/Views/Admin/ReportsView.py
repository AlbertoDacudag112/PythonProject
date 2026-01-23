"""
Views/Admin/ReportsView.py
Reports and analytics page (extracted from ReportsPage.py)
"""
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from Views.Common.StyledWidgets import StyledWidgets


class ReportsView(QWidget):
    """Reports and analytics view for admin"""

    # Signals
    view_violations_report_requested = pyqtSignal()
    export_pdf_requested = pyqtSignal()
    payment_report_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Header
        header = QLabel("Reports & Analytics")
        header.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        header.setStyleSheet("color: #e8bb41;")
        layout.addWidget(header)

        # Report buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        # View Violations Report button
        view_violations_btn = StyledWidgets.create_action_button(
            "📊 View Violations Report",
            "#9c27b0"
        )
        view_violations_btn.clicked.connect(lambda: self.view_violations_report_requested.emit())

        # Export to PDF button
        export_btn = StyledWidgets.create_action_button(
            "📄 Export Current Report (PDF)",
            "#2196f3"
        )
        export_btn.clicked.connect(lambda: self.export_pdf_requested.emit())

        # Payment Report button
        payment_report_btn = StyledWidgets.create_action_button(
            "💰 Payment Report",
            "#4caf50"
        )
        payment_report_btn.clicked.connect(lambda: self.payment_report_requested.emit())

        button_layout.addWidget(view_violations_btn)
        button_layout.addWidget(export_btn)
        button_layout.addWidget(payment_report_btn)
        button_layout.addStretch()

        layout.addLayout(button_layout)

        # Reports content area
        self.content_area = QScrollArea()
        self.content_area.setWidgetResizable(True)
        self.content_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #363636;
                border-radius: 12px;
            }
        """)

        self.content_widget = QLabel("Select a report option above to generate reports")
        self.content_widget.setFont(QFont("Segoe UI", 14))
        self.content_widget.setStyleSheet("color: #999999; padding: 50px;")
        self.content_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.content_area.setWidget(self.content_widget)
        layout.addWidget(self.content_area, 1)

    def show_violations_table(self, violations: list, statistics: dict):
        """Display violations in table format with statistics"""
        widget = QWidget()
        widget_layout = QVBoxLayout(widget)
        widget_layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("Violation Records")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #e8bb41;")
        widget_layout.addWidget(title)

        # Statistics summary
        total = statistics.get('total', 0)
        paid = statistics.get('paid', 0)
        unpaid = statistics.get('unpaid', 0)
        revenue = statistics.get('total_revenue', 0)

        summary = QLabel(
            f"Total: {total} | Paid: {paid} | Unpaid: {unpaid} | Revenue: ₱{revenue:,.2f}"
        )
        summary.setStyleSheet("color: #4caf50; font-size: 12pt; margin: 10px 0;")
        widget_layout.addWidget(summary)

        # Table
        table = QTableWidget()
        table.setColumnCount(10)
        table.setHorizontalHeaderLabels([
            "ID", "Resident", "Contact", "Plate",
            "Vehicle", "Violation", "Date",
            "Fine", "Status", "Paid Date"
        ])

        StyledWidgets.style_table(table)
        table.setRowCount(len(violations))

        for row, v in enumerate(violations):
            vehicle = f"{v['Brand']} {v['Model']}" if v['Brand'] else "N/A"
            paid_date = v['PaymentDate'] or "-"

            table.setItem(row, 0, QTableWidgetItem(v['ViolationID']))
            table.setItem(row, 1, QTableWidgetItem(v['ResidentName']))
            table.setItem(row, 2, QTableWidgetItem(v['ContactNo'] or "N/A"))
            table.setItem(row, 3, QTableWidgetItem(v['PlateNo']))
            table.setItem(row, 4, QTableWidgetItem(vehicle))
            table.setItem(row, 5, QTableWidgetItem(v['ViolationName']))
            table.setItem(row, 6, QTableWidgetItem(v['ViolationDate']))
            table.setItem(row, 7, QTableWidgetItem(f"₱{v['FineAmount']:,.2f}"))
            table.setItem(row, 8, QTableWidgetItem(v['PaymentStatus']))
            table.setItem(row, 9, QTableWidgetItem(paid_date))

        table.resizeColumnsToContents()
        widget_layout.addWidget(table)

        self.content_area.setWidget(widget)

    def show_payment_report(self, statistics: dict, recent_payments: list):
        """Display payment report summary"""
        widget = QWidget()
        widget_layout = QVBoxLayout(widget)
        widget_layout.setContentsMargins(30, 30, 30, 30)
        widget_layout.setSpacing(20)

        # Title
        title = QLabel("Payment Report")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: #e8bb41;")
        widget_layout.addWidget(title)

        # Note
        note = QLabel("Note: This is a summary view. To export violations to PDF, use 'View Violations Report' first.")
        note.setStyleSheet("color: #ff9800; font-size: 10pt; font-style: italic;")
        widget_layout.addWidget(note)

        # Statistics
        total = statistics.get('total_violations', 1) or 1
        stats_text = f"""
<b>Payment Statistics</b><br><br>
<b>Total Violations:</b> {statistics.get('total_violations', 0)}<br>
<b>Paid Violations:</b> {statistics.get('paid_count', 0)} ({statistics.get('paid_count', 0) / total * 100:.1f}%)<br>
<b>Unpaid Violations:</b> {statistics.get('unpaid_count', 0)} ({statistics.get('unpaid_count', 0) / total * 100:.1f}%)<br><br>
<b>Total Revenue Collected:</b> ₱{statistics.get('total_revenue', 0):,.2f}<br>
<b>Pending Revenue:</b> ₱{statistics.get('pending_revenue', 0):,.2f}<br>
        """
        stats_label = QLabel(stats_text)
        stats_label.setTextFormat(Qt.TextFormat.RichText)
        stats_label.setStyleSheet(
            "color: #ffffff; font-size: 12pt; background-color: #2d2d2d; padding: 20px; border-radius: 8px;"
        )
        widget_layout.addWidget(stats_label)

        # Recent payments
        recent_label = QLabel("Recent Payments")
        recent_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        recent_label.setStyleSheet("color: #e8bb41; margin-top: 20px;")
        widget_layout.addWidget(recent_label)

        # Recent payments table
        payments_table = QTableWidget()
        payments_table.setColumnCount(5)
        payments_table.setHorizontalHeaderLabels(["Payment ID", "Resident", "Violation", "Amount", "Date"])
        StyledWidgets.style_table(payments_table)

        payments_table.setRowCount(len(recent_payments))
        for row, payment in enumerate(recent_payments):
            payments_table.setItem(row, 0, QTableWidgetItem(payment['PaymentID']))
            payments_table.setItem(row, 1, QTableWidgetItem(payment['resident_name']))
            payments_table.setItem(row, 2, QTableWidgetItem(payment['ViolationName']))
            payments_table.setItem(row, 3, QTableWidgetItem(f"₱{payment['FineAmount']:,.2f}"))
            payments_table.setItem(row, 4, QTableWidgetItem(payment['payment_date']))

        widget_layout.addWidget(payments_table)

        self.content_area.setWidget(widget)

    def show_message(self, title: str, message: str, is_error: bool = False):
        """Show message dialog"""
        if is_error:
            QMessageBox.critical(self, title, message)
        else:
            QMessageBox.information(self, title, message)