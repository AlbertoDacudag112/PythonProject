import os

from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont, QCursor
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QComboBox,
    QTableWidget, QHeaderView, QTableWidgetItem, QPushButton
)

from Views.Common.StyledWidgets import StyledWidgets

# Resolve the icon path once at module level
CHEVRON_ICON = os.path.join(
    os.path.dirname(__file__), "..", "..", "Controllers", "Icons", "down-chevron.png"
).replace("\\", "/")


class ViolationsView(QWidget):
    """Violations table view"""

    # Signals
    search_changed = pyqtSignal(str)
    filter_changed = pyqtSignal(str)
    refresh_requested = pyqtSignal()
    payment_requested = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self._setup_ui()

    # ---------- helper to center widgets in table cells ----------
    def _center_widget(self, widget: QWidget) -> QWidget:
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch()
        layout.addWidget(widget)
        layout.addStretch()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return container

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Header
        header = QLabel("My Violations")
        header.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        header.setStyleSheet("color: #e8bb41;")
        layout.addWidget(header)

        # Search & filter bar
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(15)

        self.search_input = StyledWidgets.create_search_input(
            "Search by Violation ID, Vehicle Plate, or Type..."
        )
        self.search_input.textChanged.connect(
            lambda text: self.search_changed.emit(text)
        )

        status_label = QLabel("Status:")
        status_label.setFont(QFont("Segoe UI", 11))
        status_label.setStyleSheet("color: #ffffff;")

        self.status_filter = QComboBox()
        self.status_filter.addItems(["All", "Paid", "Unpaid"])
        self.status_filter.setFont(QFont("Segoe UI", 11))
        self.status_filter.setStyleSheet(f"""
            QComboBox {{
                padding: 10px 15px;
                border: 2px solid #5a5a5a;
                border-radius: 8px;
                background-color: #363636;
                color: #ffffff;
                min-width: 150px;
            }}
            QComboBox:focus {{ border: 2px solid #e8bb41; }}
            QComboBox::drop-down {{
                border: none;
                padding-right: 10px;
            }}
            QComboBox::down-arrow {{
                image: url({CHEVRON_ICON});
                width: 14px;
                height: 14px;
                margin-right: 8px;
            }}
            QComboBox QAbstractItemView {{
                background-color: #363636;
                color: #ffffff;
                selection-background-color: #e8bb41;
                selection-color: #1e1e1e;
            }}
        """)

        self.status_filter.currentTextChanged.connect(
            lambda text: self.filter_changed.emit(text)
        )

        refresh_btn = StyledWidgets.create_action_button("Refresh", "")
        refresh_btn.clicked.connect(
            lambda: self.refresh_requested.emit()
        )

        filter_layout.addWidget(self.search_input, 1)
        filter_layout.addWidget(status_label)
        filter_layout.addWidget(self.status_filter)
        filter_layout.addWidget(refresh_btn)

        layout.addLayout(filter_layout)

        # Table
        self.violations_table = QTableWidget()
        self.violations_table.setColumnCount(6)
        self.violations_table.setHorizontalHeaderLabels([
            "Violation ID", "Vehicle Plate", "Violation Type",
            "Date", "Fine Amount", "Action"
        ])

        StyledWidgets.style_table(self.violations_table)

        header = self.violations_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)

        self.violations_table.setColumnWidth(5, 160)

        # Lock row height (prevents overlap)
        v_header = self.violations_table.verticalHeader()
        v_header.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        v_header.setDefaultSectionSize(64)

        layout.addWidget(self.violations_table)

    def populate_table(self, violations: list):
        self.violations_table.setRowCount(len(violations))

        for row, violation in enumerate(violations):
            def set_item(col, text):
                item = QTableWidgetItem(str(text))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.violations_table.setItem(row, col, item)

            set_item(0, violation.get("violation_id", ""))
            set_item(1, violation.get("plate_no", ""))
            set_item(2, violation.get("violation_type", ""))
            set_item(3, violation.get("date", ""))

            fine = float(violation.get("fine_amount", 0) or 0)
            set_item(4, f"₱{fine:.2f}")

            status = violation.get("status", "Unpaid")

            if status == "Unpaid":
                btn = QPushButton("Pay")
                btn.setFixedSize(100, 40)
                btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #e8bb41;
                        color: #1e1e1e;
                        border-radius: 8px;
                        font-weight: bold;
                        font-size: 13px;
                        border: none;
                    }
                    QPushButton:hover { background-color: #f0c855; }
                    QPushButton:pressed { background-color: #d4a838; }
                """)
                btn.clicked.connect(
                    lambda _, v=violation: self.payment_requested.emit(v)
                )

                self.violations_table.setCellWidget(
                    row, 5, self._center_widget(btn)
                )

            else:
                paid = QLabel("Paid")
                paid.setFixedSize(100, 40)
                paid.setAlignment(Qt.AlignmentFlag.AlignCenter)
                paid.setStyleSheet("""
                    QLabel {
                        background-color: #2e7d32;
                        color: #ffffff;
                        border-radius: 8px;
                        font-weight: bold;
                        font-size: 13px;
                    }
                """)

                self.violations_table.setCellWidget(
                    row, 5, self._center_widget(paid)
                )