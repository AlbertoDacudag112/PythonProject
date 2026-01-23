from PyQt6.QtCore import pyqtSignal, Qt, QRegularExpression
from PyQt6.QtGui import QFont, QRegularExpressionValidator, QCursor
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QFormLayout, QComboBox, QLineEdit, QHBoxLayout, QPushButton, \
    QMessageBox


class PaymentDialog(QDialog):
    """Payment processing dialog - UI only"""

    # Signal
    payment_submitted = pyqtSignal(dict)  # form_data

    def __init__(self, violation_data: dict, parent=None):
        super().__init__(parent)
        self.violation_data = violation_data
        self.setWindowTitle("Process Payment")
        self.setFixedSize(600, 650)
        self.setModal(True)
        self.setStyleSheet("background-color: #2d2d2d;")

        self._setup_ui()

    def _setup_ui(self):
        """Initialize UI components"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)

        # Header
        header_label = QLabel("💳 Payment Processing")
        header_label.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        header_label.setStyleSheet("color: #e8bb41;")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header_label)

        main_layout.addSpacing(10)

        # Violation Info Summary
        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)

        violation_id_label = QLabel(f"Violation ID: {self.violation_data['violation_id']}")
        violation_id_label.setFont(QFont("Segoe UI", 11))
        violation_id_label.setStyleSheet("color: #cccccc;")
        violation_id_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        plate_label = QLabel(f"Vehicle: {self.violation_data['plate_no']} • {self.violation_data['violation_type']}")
        plate_label.setFont(QFont("Segoe UI", 11))
        plate_label.setStyleSheet("color: #cccccc;")
        plate_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        amount_display = QLabel(f"₱{self.violation_data['fine_amount']:.2f}")
        amount_display.setFont(QFont("Segoe UI", 36, QFont.Weight.Bold))
        amount_display.setStyleSheet("color: #4caf50;")
        amount_display.setAlignment(Qt.AlignmentFlag.AlignCenter)

        info_layout.addWidget(violation_id_label)
        info_layout.addWidget(plate_label)
        info_layout.addWidget(amount_display)

        main_layout.addLayout(info_layout)
        main_layout.addSpacing(20)

        # Form
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignTop)

        # Payment Method
        payment_type_label = self._create_label("Payment Method *")

        self.payment_type_combo = QComboBox()
        self.payment_type_combo.addItems([
            "Cash", "Credit Card", "Debit Card",
            "GCash", "PayMaya", "Bank Transfer"
        ])
        self.payment_type_combo.setFixedHeight(42)
        self._style_combo(self.payment_type_combo)
        self.payment_type_combo.currentTextChanged.connect(self._on_payment_type_changed)

        # Reference Number
        reference_label = self._create_label("Reference Number")

        self.reference_input = QLineEdit()
        self.reference_input.setPlaceholderText("Enter reference/transaction number")
        self._style_input(self.reference_input)
        self.reference_input.setEnabled(False)

        # Payer Name
        payer_label = self._create_label("Payer Name *")

        self.payer_input = QLineEdit()
        self.payer_input.setPlaceholderText("Enter your full name")
        self._style_input(self.payer_input)

        # Contact Number
        contact_label = self._create_label("Contact Number *")

        self.contact_input = QLineEdit()
        self.contact_input.setPlaceholderText("Enter 11-digit contact number (09xxxxxxxxx)")
        self._style_input(self.contact_input)

        # Validator for contact
        contact_validator = QRegularExpressionValidator(QRegularExpression("[0-9]{0,11}"))
        self.contact_input.setValidator(contact_validator)
        self.contact_input.setMaxLength(11)

        # Add to form
        form_layout.addRow(payment_type_label, self.payment_type_combo)
        form_layout.addRow(reference_label, self.reference_input)
        form_layout.addRow(payer_label, self.payer_input)
        form_layout.addRow(contact_label, self.contact_input)

        main_layout.addLayout(form_layout)
        main_layout.addStretch()

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        cancel_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        cancel_btn.setStyleSheet("""
            QPushButton {
                padding: 15px 40px;
                background-color: #5a5a5a;
                color: #ffffff;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #6a6a6a;
            }
        """)
        cancel_btn.clicked.connect(self.reject)

        self.process_btn = QPushButton("Process Payment")
        self.process_btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.process_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.process_btn.setStyleSheet("""
            QPushButton {
                padding: 15px 40px;
                background-color: #4caf50;
                color: #ffffff;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #66bb6a;
            }
            QPushButton:pressed {
                background-color: #388e3c;
            }
        """)
        self.process_btn.clicked.connect(self._handle_process)

        button_layout.addStretch()
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(self.process_btn)

        main_layout.addLayout(button_layout)

    def _create_label(self, text: str):
        """Create form label"""
        label = QLabel(text)
        label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        label.setStyleSheet("color: #ffffff;")
        return label

    def _style_input(self, widget):
        """Style input field"""
        widget.setFont(QFont("Segoe UI", 11))
        widget.setFixedHeight(42)
        widget.setStyleSheet("""
            QLineEdit {
                padding: 8px 10px;
                border: 2px solid #5a5a5a;
                border-radius: 8px;
                background-color: #363636;
                color: #ffffff;
            }
            QLineEdit:focus {
                border: 2px solid #e8bb41;
                background-color: #404040;
            }
            QLineEdit:disabled {
                background-color: #2a2a2a;
                color: #777777;
            }
        """)

    def _style_combo(self, widget):
        """Style combo box"""
        widget.setStyleSheet("""
            QComboBox {
                padding: 8px 36px 8px 10px;
                border: 2px solid #5a5a5a;
                border-radius: 8px;
                background-color: #363636;
                color: #ffffff;
            }
            QComboBox:focus {
                border: 2px solid #e8bb41;
                background-color: #404040;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 28px;
                border-left: 1px solid #5a5a5a;
            }
            QComboBox::down-arrow {
                image: none;
                width: 0;
                height: 0;
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-top: 7px solid #cccccc;
                margin-right: 10px;
            }
            QComboBox::down-arrow:on {
                border-top: 7px solid #e8bb41;
            }
            QComboBox QAbstractItemView {
                background-color: #363636;
                color: #ffffff;
                selection-background-color: #e8bb41;
                selection-color: #1e1e1e;
                border: 1px solid #5a5a5a;
                padding: 6px;
            }
        """)

    def _on_payment_type_changed(self, payment_type: str):
        """Enable/disable reference based on payment type"""
        online_methods = ["GCash", "PayMaya", "Bank Transfer", "Credit Card", "Debit Card"]
        self.reference_input.setEnabled(payment_type in online_methods)

        if payment_type in online_methods:
            self.reference_input.setPlaceholderText(f"Enter {payment_type} reference number *")
        else:
            self.reference_input.clear()
            self.reference_input.setPlaceholderText("Not applicable for cash payments")

    def _handle_process(self):
        """Emit payment submission signal"""
        form_data = {
            'payment_type': self.payment_type_combo.currentText(),
            'reference': self.reference_input.text().strip(),
            'payer_name': self.payer_input.text().strip(),
            'contact': self.contact_input.text().strip()
        }
        self.payment_submitted.emit(form_data)

    def show_error(self, message: str):
        """Show error message"""
        QMessageBox.warning(self, "Validation Error", message)

    def show_confirmation(self, amount: float, payment_type: str, payer: str, contact: str) -> bool:
        """Show payment confirmation dialog"""
        reply = QMessageBox.question(
            self,
            "Confirm Payment",
            f"Process payment of ₱{amount:.2f}?\n\n"
            f"Payment Method: {payment_type}\n"
            f"Payer: {payer}\n"
            f"Contact: {contact}\n\n"
            "This action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        return reply == QMessageBox.StandardButton.Yes

    def show_success(self, receipt_no: str, amount: float):
        """Show success message"""
        QMessageBox.information(
            self,
            "Payment Successful",
            f"Payment has been processed successfully!\n\n"
            f"Violation ID: {self.violation_data['violation_id']}\n"
            f"Amount: ₱{amount:.2f}\n"
            f"Receipt: {receipt_no}\n\n"
            "Thank you for your payment!"
        )