"""
Main/RoadEyeMain.py
Application entry point - wires all MVC components together
"""
import sys
from PyQt6.QtWidgets import QApplication, QMessageBox, QDialog, QFileDialog
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

# Controllers
from Controllers.AuthController import AuthController
from Controllers.ResidentController import ResidentController
from Controllers.AdminController import AdminController
from Controllers.PaymentController import PaymentController
from Controllers.ViolationController import ViolationController
from Controllers.VehicleController import VehicleController
from Controllers.ReportController import ReportController

# Views - Auth
from Views.Auth.LoginView import LoginView
from Views.Auth.SignUpView import SignUpView

# Views - Resident
from Views.Resident.ResidentMainView import ResidentMainView
from Views.Resident.DashboardView import DashboardView
from Views.Resident.ViolationsView import ViolationsView
from Views.Resident.ViolationHistoryView import ViolationHistoryView
from Views.Resident.PaymentHistoryView import PaymentHistoryView
from Views.Resident.PaymentDialog import PaymentDialog

# Views - Admin
from Views.Admin.AdminMainView import AdminMainView
from Views.Admin.AdminDashboardView import AdminDashboardView
from Views.Admin.ViolationsManagementView import ViolationsManagementView
from Views.Admin.ResidentsManagementView import ResidentsManagementView
from Views.Admin.VehiclesManagementView import VehiclesManagementView
from Views.Admin.ReportsView import ReportsView
from Views.Admin.AddVehicleDialog import AddVehicleDialog
from Views.Admin.EditVehicleDialog import EditVehicleDialog
from Views.Admin.AddViolationDialog import AddViolationDialog

# Utilities
from Controllers.Utility.ChartGenerator import ChartGenerator

from datetime import datetime


class Application:
    """Main application coordinator"""

    def __init__(self):
        self.auth_controller = AuthController()
        self.current_window = None

    def start(self):
        """Show login window"""
        print("   → Creating AuthController...")
        print("   → Creating LoginView...")
        self.login_view = LoginView()
        print("   → LoginView created successfully")

        print("   → Connecting signals...")
        self.login_view.login_requested.connect(self.handle_login)
        self.login_view.signup_requested.connect(self.show_signup)
        print("   → Signals connected")

        print("   → Showing login window...")
        self.login_view.show()
        print("   → Login window shown")

        self.current_window = self.login_view

    def handle_login(self, username: str, password: str):
        """Handle login attempt"""
        user_data, error = self.auth_controller.login(username, password)

        if error:
            self.login_view.show_error(error)
            self.login_view.clear_password()
            return

        if user_data['user_type'] == 'admin':
            self.show_admin_window(user_data)
        else:
            self.show_resident_window(user_data)

    def show_signup(self):
        """Show signup dialog"""
        signup_view = SignUpView(self.login_view)
        signup_view.signup_submitted.connect(
            lambda form_data: self.handle_signup(form_data, signup_view)
        )

        if signup_view.exec() == QDialog.DialogCode.Accepted:
            self.login_view.show_info(
                "Sign Up Complete",
                "You can now log in with your new account!"
            )

    def handle_signup(self, form_data: dict, signup_dialog: SignUpView):
        """Handle signup submission"""
        success, message = self.auth_controller.register(form_data)

        if success:
            signup_dialog.accept()
        else:
            signup_dialog.show_message("Registration Failed", message, is_error=True)

    def show_resident_window(self, user_data: dict):
        """Open resident window with all pages configured"""
        controller = ResidentController(user_data)
        payment_controller = PaymentController()

        resident_window = ResidentMainView(user_data)

        dashboard = DashboardView()
        violations = ViolationsView()
        violation_history = ViolationHistoryView()
        payment_history = PaymentHistoryView()

        resident_window.add_page(dashboard)
        resident_window.add_page(violations)
        resident_window.add_page(violation_history)
        resident_window.add_page(payment_history)

        stats = controller.get_dashboard_stats()
        dashboard.update_statistics(stats)

        monthly_data = controller.get_monthly_chart_data()
        chart = ChartGenerator.create_resident_dashboard_chart(monthly_data)
        dashboard.update_chart(chart)

        violations_data = controller.get_violations()
        violations.populate_table(violations_data)

        def handle_violations_search(text):
            status_filter = violations.status_filter.currentText()
            filtered = controller.filter_violations(violations_data, text, status_filter)
            violations.populate_table(filtered)

        def handle_violations_filter(status):
            search_text = violations.search_input.text()
            filtered = controller.filter_violations(violations_data, search_text, status)
            violations.populate_table(filtered)

        def handle_violations_refresh():
            nonlocal violations_data
            violations_data = controller.get_violations()
            violations.populate_table(violations_data)

        def handle_payment_request(violation_data):
            payment_dialog = PaymentDialog(violation_data, resident_window)
            payment_dialog.payment_submitted.connect(
                lambda form_data: self.process_resident_payment(
                    payment_controller, violation_data, form_data, payment_dialog, resident_window, controller
                )
            )
            payment_dialog.exec()

        violations.search_changed.connect(handle_violations_search)
        violations.filter_changed.connect(handle_violations_filter)
        violations.refresh_requested.connect(handle_violations_refresh)
        violations.payment_requested.connect(handle_payment_request)

        all_violations = controller.get_violations()
        violation_history.populate_table(all_violations)

        def _apply_history_filters():
            """Apply all three filters (search, year, status) together"""
            search_text = violation_history.search_input.text()
            year = violation_history.year_filter.currentText()
            status = violation_history.status_filter.currentText()

            filtered = controller.filter_violations(all_violations, search_text, status)

            if year and year != "All Years":
                filtered = [v for v in filtered if str(v.get('date', '')).startswith(year)]

            violation_history.populate_table(filtered)

        def handle_history_year_filter(year):
            _apply_history_filters()

        def handle_history_status_filter(status):
            _apply_history_filters()

        violation_history.search_changed.connect(lambda text: _apply_history_filters())
        violation_history.year_filter_changed.connect(handle_history_year_filter)
        violation_history.status_filter_changed.connect(handle_history_status_filter)

        payments = controller.get_payment_history()
        payment_history.populate_table(payments)

        def handle_page_change(index):
            if index == 0:
                stats = controller.get_dashboard_stats()
                dashboard.update_statistics(stats)
                monthly_data = controller.get_monthly_chart_data()
                chart = ChartGenerator.create_resident_dashboard_chart(monthly_data)
                dashboard.update_chart(chart)
            elif index == 2:
                all_violations = controller.get_violations()
                violation_history.populate_table(all_violations)
            elif index == 3:
                payments = controller.get_payment_history()
                payment_history.populate_table(payments)

        resident_window.page_changed.connect(handle_page_change)
        resident_window.logout_requested.connect(
            lambda: self._handle_logout(resident_window, user_data)
        )

        resident_window.show()
        self.login_view.close()
        self.current_window = resident_window

    def process_resident_payment(self, payment_controller, violation_data, form_data, dialog, window, controller):
        """Process payment submission"""
        is_valid, error_msg = payment_controller.validate_payment_form(form_data)
        if not is_valid:
            dialog.show_error(error_msg)
            return

        if not dialog.show_confirmation(
                violation_data['fine_amount'],
                form_data['payment_type'],
                form_data['payer_name'],
                form_data['contact']
        ):
            return

        success, result = payment_controller.process_payment(violation_data, form_data)

        if success:
            dialog.show_success(result['receipt_no'], result['amount'])
            dialog.accept()

            violations_view = window.stacked_widget.widget(1)
            violations_data = controller.get_violations()
            violations_view.populate_table(violations_data)

            dashboard_view = window.stacked_widget.widget(0)
            stats = controller.get_dashboard_stats()
            dashboard_view.update_statistics(stats)
        else:
            dialog.show_error(result)

    def show_admin_window(self, admin_data: dict):
        """Open admin window with all pages configured"""
        admin_controller = AdminController(admin_data)
        violation_controller = ViolationController()
        vehicle_controller = VehicleController()
        report_controller = ReportController()

        admin_controller.initialize_database()

        admin_window = AdminMainView(admin_data)

        dashboard = AdminDashboardView()
        violations = ViolationsManagementView()
        residents = ResidentsManagementView()
        vehicles = VehiclesManagementView()
        reports = ReportsView()

        admin_window.add_page(dashboard)
        admin_window.add_page(violations)
        admin_window.add_page(residents)
        admin_window.add_page(vehicles)
        admin_window.add_page(reports)

        stats = admin_controller.get_dashboard_statistics()
        dashboard.update_statistics(stats)

        monthly_data = admin_controller.get_monthly_chart_data()
        chart = ChartGenerator.create_admin_dashboard_chart(monthly_data)
        dashboard.update_chart(chart)

        violations_data = violation_controller.get_all_violations()
        violations.populate_table(violations_data)

        violations.search_changed.connect(
            lambda text: violations.populate_table(
                violation_controller.search_violations(violations_data, text)
            )
        )
        violations.refresh_requested.connect(
            lambda: self._refresh_violations(violation_controller, violations)
        )
        violations.add_violation_requested.connect(
            lambda: self._show_add_violation_dialog(violation_controller, vehicle_controller, violations, admin_window)
        )
        violations.view_violation_requested.connect(
            lambda v_id: self._show_violation_details(violation_controller, v_id, admin_window)
        )

        residents_data = admin_controller.get_all_residents()
        residents.populate_table(residents_data)

        residents.search_changed.connect(
            lambda text: residents.populate_table(
                admin_controller.search_residents(residents_data, text)
            )
        )
        residents.view_resident_requested.connect(
            lambda r_id: self._show_resident_details(admin_controller, r_id, admin_window)
        )

        vehicles_data = vehicle_controller.get_all_vehicles()
        vehicles.populate_table(vehicles_data)

        vehicles.search_changed.connect(
            lambda text: vehicles.populate_table(
                vehicle_controller.search_vehicles(vehicles_data, text)
            )
        )
        vehicles.add_vehicle_requested.connect(
            lambda: self._show_add_vehicle_dialog(vehicle_controller, admin_controller, vehicles, admin_window)
        )
        vehicles.edit_vehicle_requested.connect(
            lambda v_id: self._show_edit_vehicle_dialog(vehicle_controller, v_id, vehicles, admin_window)
        )
        vehicles.view_vehicle_requested.connect(
            lambda v_id: self._show_vehicle_details(vehicle_controller, v_id, admin_window)
        )

        reports.view_violations_report_requested.connect(
            lambda: self._show_violations_report(report_controller, reports)
        )
        reports.export_pdf_requested.connect(
            lambda: self._export_violations_pdf(report_controller, reports, admin_window)
        )
        reports.payment_report_requested.connect(
            lambda: self._show_payment_report(report_controller, reports)
        )

        def handle_page_change(index):
            if index == 0:
                stats = admin_controller.get_dashboard_statistics()
                dashboard.update_statistics(stats)
                year = dashboard.get_selected_year()
                monthly_data = admin_controller.get_monthly_chart_data(year=year)
                chart = ChartGenerator.create_admin_dashboard_chart(monthly_data)
                dashboard.update_chart(chart)

        def handle_year_filter_changed(year: int):
            monthly_data = admin_controller.get_monthly_chart_data(year=year)
            chart = ChartGenerator.create_admin_dashboard_chart(monthly_data)
            dashboard.update_chart(chart)

        dashboard.year_filter_changed.connect(handle_year_filter_changed)
        admin_window.page_changed.connect(handle_page_change)
        admin_window.logout_requested.connect(
            lambda: self._handle_logout(admin_window, admin_data)
        )

        admin_window.show()
        self.login_view.close()
        self.current_window = admin_window

    def _refresh_violations(self, controller, view):
        violations_data = controller.get_all_violations()
        view.populate_table(violations_data)

    def _show_add_violation_dialog(self, violation_controller, vehicle_controller, violations_view, parent):
        vehicles_list = vehicle_controller.get_vehicles_for_dropdown()
        types_list = violation_controller.get_violation_types()

        dialog = AddViolationDialog(vehicles_list, types_list, parent)
        dialog.violation_submitted.connect(
            lambda form_data: self._handle_add_violation(
                violation_controller, form_data, dialog, violations_view
            )
        )
        dialog.exec()

    def _handle_add_violation(self, controller, form_data, dialog, view):
        success, message = controller.add_violation(
            form_data['vehicle_id'],
            form_data['violation_type_id'],
            form_data['violation_date']
        )

        if success:
            QMessageBox.information(dialog, "Success", message)
            dialog.accept()
            self._refresh_violations(controller, view)
        else:
            dialog.show_error(message)

    def _show_violation_details(self, controller, violation_id, parent):
        violation = controller.get_violation_details(violation_id)

        if violation:
            details = f"""
<b>Violation Details</b><br><br>
<b>Violation ID:</b> {violation['ViolationID']}<br>
<b>Date:</b> {violation['ViolationDate']}<br>
<b>Type:</b> {violation['ViolationName']}<br>
<b>Fine Amount:</b> ₱{violation['FineAmount']:.2f}<br><br>

<b>Vehicle Information</b><br>
<b>Plate Number:</b> {violation['PlateNo']}<br>
<b>Brand/Model:</b> {violation['Brand']} {violation['Model']}<br><br>

<b>Owner Information</b><br>
<b>Name:</b> {violation['resident_name']}<br>
<b>Contact:</b> {violation['ContactNo']}<br><br>

<b>Payment Status:</b> {violation['status']}<br>
"""
            if violation['PaymentDate']:
                details += f"<b>Payment Date:</b> {violation['PaymentDate']}<br>"

            msg = QMessageBox(parent)
            msg.setWindowTitle("Violation Details")
            msg.setTextFormat(Qt.TextFormat.RichText)
            msg.setText(details)
            msg.exec()

    def _show_add_vehicle_dialog(self, vehicle_controller, admin_controller, vehicles_view, parent):
        residents_list = admin_controller.get_all_residents()

        dialog = AddVehicleDialog(residents_list, parent)
        dialog.vehicle_submitted.connect(
            lambda form_data: self._handle_add_vehicle(
                vehicle_controller, form_data, dialog, vehicles_view
            )
        )
        dialog.exec()

    def _handle_add_vehicle(self, controller, form_data, dialog, view):
        success, message = controller.add_vehicle(
            form_data['resident_id'],
            form_data['plate_no'],
            form_data['brand'],
            form_data['model'],
            form_data['color']
        )

        if success:
            QMessageBox.information(dialog, "Success", message)
            dialog.accept()
            vehicles_data = controller.get_all_vehicles()
            view.populate_table(vehicles_data)
        else:
            dialog.show_error(message)

    def _show_edit_vehicle_dialog(self, controller, vehicle_id, vehicles_view, parent):
        vehicle_data = controller.get_vehicle_details(vehicle_id)

        if not vehicle_data:
            QMessageBox.warning(parent, "Not Found", "Vehicle not found")
            return

        dialog = EditVehicleDialog(vehicle_data, parent)
        dialog.vehicle_updated.connect(
            lambda form_data: self._handle_update_vehicle(
                controller, form_data, dialog, vehicles_view
            )
        )
        dialog.exec()

    def _handle_update_vehicle(self, controller, form_data, dialog, view):
        success, message = controller.update_vehicle(
            form_data['vehicle_id'],
            form_data['brand'],
            form_data['model'],
            form_data['color']
        )

        if success:
            QMessageBox.information(dialog, "Success", message)
            dialog.accept()
            vehicles_data = controller.get_all_vehicles()
            view.populate_table(vehicles_data)
        else:
            dialog.show_error(message)

    def _show_vehicle_details(self, controller, vehicle_id, parent):
        vehicle_data = controller.get_vehicle_details(vehicle_id)

        if not vehicle_data:
            QMessageBox.warning(parent, "Not Found", "Vehicle not found")
            return

        details = f"""
<b>Vehicle Information</b><br><br>
<b>Vehicle ID:</b> {vehicle_data.get('VehicleID', 'N/A')}<br>
<b>Plate Number:</b> {vehicle_data.get('PlateNo', 'N/A')}<br>
<b>Brand:</b> {vehicle_data.get('Brand', 'N/A')}<br>
<b>Model:</b> {vehicle_data.get('Model', 'N/A')}<br>
<b>Color:</b> {vehicle_data.get('Color', 'N/A')}<br><br>

<b>Owner Information</b><br>
<b>Resident ID:</b> {vehicle_data.get('ResidentID', 'N/A')}<br>
<b>Owner Name:</b> {vehicle_data.get('owner_name', 'N/A')}<br>
"""

        msg = QMessageBox(parent)
        msg.setWindowTitle("Vehicle Details")
        msg.setTextFormat(Qt.TextFormat.RichText)
        msg.setText(details)
        msg.exec()

    def _show_resident_details(self, controller, resident_id, parent):
        """Show resident details — fixed to use separate name fields"""
        resident, vehicles = controller.get_resident_details(resident_id)

        if resident:
            # Build full name from separate fields
            first = resident.get('first_name') or resident.get('RFirstName', '')
            middle = resident.get('middle_name') or resident.get('RMiddleName', '')
            last = resident.get('last_name') or resident.get('RLastName', '')
            parts = [first, middle, last] if middle else [first, last]
            full_name = ' '.join(p for p in parts if p).strip()

            details = f"""
<b>Resident Information</b><br><br>
<b>Resident ID:</b> {resident['ResidentID']}<br>
<b>Name:</b> {full_name}<br>
<b>Sex:</b> {resident['Sex']}<br>
<b>Contact Number:</b> {resident['ContactNo']}<br>
<b>Address:</b> {resident.get('Address') or 'N/A'}<br><br>

<b>Statistics</b><br>
<b>Registered Vehicles:</b> {resident.get('vehicle_count', 0)}<br>
<b>Total Violations:</b> {resident.get('violation_count', 0)}<br>
<b>Paid Violations:</b> {resident.get('paid_count') or 0}<br>
<b>Unpaid Violations:</b> {resident.get('unpaid_count') or 0}<br>
"""
            if vehicles:
                details += "<br><b>Registered Vehicles:</b><br>"
                for vehicle in vehicles:
                    details += f"• {vehicle['PlateNo']} - {vehicle['Brand']} {vehicle['Model']}<br>"

            msg = QMessageBox(parent)
            msg.setWindowTitle("Resident Details")
            msg.setTextFormat(Qt.TextFormat.RichText)
            msg.setText(details)
            msg.exec()

    def _show_violations_report(self, controller, view):
        violations = controller.get_violations_report_data()
        stats = controller.calculate_report_statistics(violations)
        view.show_violations_table(violations, stats)

    def _export_violations_pdf(self, controller, view, parent):
        violations = controller.get_violations_report_data()

        if not violations:
            view.show_message("No Data", "No violations data to export", is_error=True)
            return

        file_path, _ = QFileDialog.getSaveFileName(
            parent,
            "Export Violations Report",
            f"violations_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            "PDF Files (*.pdf)"
        )

        if file_path:
            success, message = controller.export_violations_report_to_pdf(file_path, violations)
            view.show_message(
                "Export " + ("Successful" if success else "Failed"),
                message,
                is_error=not success
            )

    def _show_payment_report(self, controller, view):
        stats, recent_payments = controller.get_payment_report_data()
        view.show_payment_report(stats, recent_payments)

    def _handle_logout(self, window, user_data: dict):
        self.auth_controller.logout(user_data)
        window.close()
        self.start()


def main():
    """Application entry point with debug logging"""
    try:
        print("=" * 60)
        print("STARTING ROADEYE APPLICATION")
        print("=" * 60)

        print("1. Creating QApplication...")
        app = QApplication(sys.argv)
        print("   ✓ QApplication created")

        print("2. Setting font...")
        app.setFont(QFont("Segoe UI", 10))
        print("   ✓ Font set")

        print("3. Creating Application instance...")
        application = Application()
        print("   ✓ Application instance created")

        print("4. Starting application (showing login)...")
        application.start()
        print("   ✓ Login window should be visible")

        print("5. Entering event loop...")
        sys.exit(app.exec())

    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ FATAL ERROR OCCURRED")
        print("=" * 60)
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Message: {e}")
        print("\nFull Traceback:")
        print("-" * 60)
        import traceback
        traceback.print_exc()
        print("=" * 60)
        input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()