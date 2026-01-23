"""
Main/RoadEyeMain.py
Application entry point - wires all MVC components together
"""
import sys
from PyQt6.QtWidgets import QApplication, QMessageBox, QDialog, QFileDialog
from PyQt6.QtGui import QFont

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
        self.login_view = LoginView()

        # Connect signals
        self.login_view.login_requested.connect(self.handle_login)
        self.login_view.signup_requested.connect(self.show_signup)

        self.login_view.show()
        self.current_window = self.login_view

    def handle_login(self, username: str, password: str):
        """Handle login attempt"""
        user_data, error = self.auth_controller.login(username, password)

        if error:
            self.login_view.show_error(error)
            self.login_view.clear_password()
            return

        # Check user type and open appropriate window
        if user_data['user_type'] == 'admin':
            self.show_admin_window(user_data)
        else:
            self.show_resident_window(user_data)

    def show_signup(self):
        """Show signup dialog"""
        signup_view = SignUpView(self.login_view)
        signup_view.signup_submitted.connect(self.handle_signup)

        if signup_view.exec() == QDialog.DialogCode.Accepted:
            self.login_view.show_info(
                "Sign Up Complete",
                "You can now log in with your new account!"
            )

    def handle_signup(self, form_data: dict):
        """Handle signup submission"""
        success, message = self.auth_controller.register(form_data)

        sender = self.sender()
        if success:
            sender.accept()  # Close signup dialog
        else:
            sender.show_message("Registration Failed", message, is_error=True)

    def show_resident_window(self, user_data: dict):
        """Open resident window with all pages configured"""
        # Create controller
        controller = ResidentController(user_data)
        payment_controller = PaymentController()

        # Create main window
        resident_window = ResidentMainView(user_data)

        # Create pages
        dashboard = DashboardView()
        violations = ViolationsView()
        payment_history = PaymentHistoryView()

        # Add pages to window
        resident_window.add_page(dashboard)
        resident_window.add_page(violations)
        resident_window.add_page(payment_history)

        # Setup dashboard
        stats = controller.get_dashboard_stats()
        dashboard.update_statistics(stats)

        monthly_data = controller.get_monthly_chart_data()
        chart = ChartGenerator.create_resident_dashboard_chart(monthly_data)
        dashboard.update_chart(chart)

        # Setup violations page
        violations_data = controller.get_violations()
        violations.populate_table(violations_data)

        # Connect violations page signals
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

        # Setup payment history
        payments = controller.get_payment_history()
        payment_history.populate_table(payments)

        # Connect page change signal to refresh data
        def handle_page_change(index):
            if index == 0:  # Dashboard
                stats = controller.get_dashboard_stats()
                dashboard.update_statistics(stats)
                monthly_data = controller.get_monthly_chart_data()
                chart = ChartGenerator.create_resident_dashboard_chart(monthly_data)
                dashboard.update_chart(chart)
            elif index == 2:  # Payment History
                payments = controller.get_payment_history()
                payment_history.populate_table(payments)

        resident_window.page_changed.connect(handle_page_change)

        # Connect logout
        resident_window.logout_requested.connect(
            lambda: self._handle_logout(resident_window, user_data)
        )

        # Show window
        resident_window.show()
        self.login_view.close()
        self.current_window = resident_window

    def process_resident_payment(self, payment_controller, violation_data, form_data, dialog, window, controller):
        """Process payment submission"""
        # Validate
        is_valid, error_msg = payment_controller.validate_payment_form(form_data)
        if not is_valid:
            dialog.show_error(error_msg)
            return

        # Show confirmation
        if not dialog.show_confirmation(
                violation_data['fine_amount'],
                form_data['payment_type'],
                form_data['payer_name'],
                form_data['contact']
        ):
            return

        # Process payment
        success, result = payment_controller.process_payment(violation_data, form_data)

        if success:
            dialog.show_success(result['receipt_no'], result['amount'])
            dialog.accept()

            # Refresh all data
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
        # Create controllers
        admin_controller = AdminController(admin_data)
        violation_controller = ViolationController()
        vehicle_controller = VehicleController()
        report_controller = ReportController()

        # Initialize database
        admin_controller.initialize_database()

        # Create main window
        admin_window = AdminMainView(admin_data)

        # Create pages
        dashboard = AdminDashboardView()
        violations = ViolationsManagementView()
        residents = ResidentsManagementView()
        vehicles = VehiclesManagementView()
        reports = ReportsView()

        # Add pages
        admin_window.add_page(dashboard)
        admin_window.add_page(violations)
        admin_window.add_page(residents)
        admin_window.add_page(vehicles)
        admin_window.add_page(reports)

        # Setup dashboard
        stats = admin_controller.get_dashboard_statistics()
        dashboard.update_statistics(stats)

        monthly_data = admin_controller.get_monthly_chart_data()
        chart = ChartGenerator.create_admin_dashboard_chart(monthly_data)
        dashboard.update_chart(chart)

        # Setup violations page
        violations_data = violation_controller.get_all_violations()
        violations.populate_table(violations_data)

        # Connect violations signals
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

        # Setup residents page
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

        # Setup vehicles page
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

        # Setup reports page
        reports.view_violations_report_requested.connect(
            lambda: self._show_violations_report(report_controller, reports)
        )
        reports.export_pdf_requested.connect(
            lambda: self._export_violations_pdf(report_controller, reports, admin_window)
        )
        reports.payment_report_requested.connect(
            lambda: self._show_payment_report(report_controller, reports)
        )

        # Connect page refresh
        def handle_page_change(index):
            if index == 0:  # Dashboard
                stats = admin_controller.get_dashboard_statistics()
                dashboard.update_statistics(stats)
                monthly_data = admin_controller.get_monthly_chart_data()
                chart = ChartGenerator.create_admin_dashboard_chart(monthly_data)
                dashboard.update_chart(chart)

        admin_window.page_changed.connect(handle_page_change)

        # Connect logout
        admin_window.logout_requested.connect(
            lambda: self._handle_logout(admin_window, admin_data)
        )

        # Show window
        admin_window.show()
        self.login_view.close()
        self.current_window = admin_window

    def _refresh_violations(self, controller, view):
        """Refresh violations table"""
        violations_data = controller.get_all_violations()
        view.populate_table(violations_data)

    def _show_add_violation_dialog(self, violation_controller, vehicle_controller, violations_view, parent):
        """Show add violation dialog"""
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
        """Handle violation submission"""
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
        """Show violation details"""
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
            msg.setTextFormat(1)  # RichText
            msg.setText(details)
            msg.exec()

    def _show_add_vehicle_dialog(self, vehicle_controller, admin_controller, vehicles_view, parent):
        """Show add vehicle dialog"""
        residents_list = admin_controller.get_all_residents()

        dialog = AddVehicleDialog(residents_list, parent)
        dialog.vehicle_submitted.connect(
            lambda form_data: self._handle_add_vehicle(
                vehicle_controller, form_data, dialog, vehicles_view
            )
        )
        dialog.exec()

    def _handle_add_vehicle(self, controller, form_data, dialog, view):
        """Handle vehicle submission"""
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
        """Show edit vehicle dialog"""
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
        """Handle vehicle update"""
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

    def _show_resident_details(self, controller, resident_id, parent):
        """Show resident details"""
        resident, vehicles = controller.get_resident_details(resident_id)

        if resident:
            details = f"""
<b>Resident Information</b><br><br>
<b>Resident ID:</b> {resident['ResidentID']}<br>
<b>Name:</b> {resident['full_name']}<br>
<b>Sex:</b> {resident['Sex']}<br>
<b>Contact Number:</b> {resident['ContactNo']}<br>
<b>Address:</b> {resident['Address'] or 'N/A'}<br><br>

<b>Statistics</b><br>
<b>Registered Vehicles:</b> {resident['vehicle_count']}<br>
<b>Total Violations:</b> {resident['violation_count']}<br>
<b>Paid Violations:</b> {resident['paid_count'] or 0}<br>
<b>Unpaid Violations:</b> {resident['unpaid_count'] or 0}<br>
"""
            if vehicles:
                details += "<br><b>Registered Vehicles:</b><br>"
                for vehicle in vehicles:
                    details += f"• {vehicle['PlateNo']} - {vehicle['Brand']} {vehicle['Model']}<br>"

            msg = QMessageBox(parent)
            msg.setWindowTitle("Resident Details")
            msg.setTextFormat(1)
            msg.setText(details)
            msg.exec()

    def _show_violations_report(self, controller, view):
        """Show violations report"""
        violations = controller.get_violations_report_data()
        stats = controller.calculate_report_statistics(violations)
        view.show_violations_table(violations, stats)

    def _export_violations_pdf(self, controller, view, parent):
        """Export violations to PDF"""
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
        """Show payment report"""
        stats, recent_payments = controller.get_payment_report_data()
        view.show_payment_report(stats, recent_payments)

    def _handle_logout(self, window, user_data: dict):
        """Handle logout"""
        self.auth_controller.logout(user_data)
        window.close()
        self.start()  # Show login again


def main():
    """Application entry point"""
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))

    application = Application()
    application.start()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()