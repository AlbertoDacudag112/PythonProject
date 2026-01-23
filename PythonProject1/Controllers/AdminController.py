from Models.Database import Database
from Models.ResidentModel import ResidentModel
from Models.VehicleModel import VehicleModel
from Models.ViolationModel import ViolationModel
from Models.PaymentModel import PaymentModel


class AdminController:
    """Handles admin dashboard and operations business logic"""

    def __init__(self, admin_data: dict):
        self.admin_data = admin_data
        self.db = Database(host='localhost', database='RoadEyeDB', user='root', password='')
        self.resident_model = ResidentModel(self.db)
        self.vehicle_model = VehicleModel(self.db)
        self.violation_model = ViolationModel(self.db)
        self.payment_model = PaymentModel(self.db)

    def initialize_database(self):
        """Check and apply database migrations"""
        return self.db.check_and_migrate()

    def get_dashboard_statistics(self):
        """Get all statistics for admin dashboard"""
        # Get violation statistics
        total_violations, unpaid_violations = self.violation_model.get_violation_statistics()
        paid_violations = total_violations - unpaid_violations

        # Get payment statistics
        payment_stats = self.payment_model.get_payment_statistics()

        # Get resident and vehicle counts
        total_residents = self.resident_model.get_total_residents()
        total_vehicles = self.vehicle_model.get_total_vehicles()

        return {
            'total_violations': total_violations,
            'paid_violations': paid_violations,
            'unpaid_violations': unpaid_violations,
            'total_revenue': payment_stats['total_revenue'],
            'total_residents': total_residents,
            'total_vehicles': total_vehicles
        }

    def get_monthly_chart_data(self):
        """Get monthly violations data for dashboard chart"""
        return self.violation_model.get_monthly_violations()

    def get_all_residents(self):
        """Get all residents with statistics"""
        return self.resident_model.get_all_residents()

    def get_resident_details(self, resident_id: str):
        """Get detailed resident information"""
        resident = self.resident_model.get_resident_details(resident_id)
        vehicles = self.resident_model.get_resident_vehicles(resident_id)

        return resident, vehicles

    def search_residents(self, residents: list, search_text: str):
        """Filter residents based on search text"""
        if not search_text:
            return residents

        search_lower = search_text.lower()
        filtered = []

        for resident in residents:
            # Search across multiple fields
            if (search_lower in str(resident.get('ResidentID', '')).lower() or
                    search_lower in str(resident.get('full_name', '')).lower() or
                    search_lower in str(resident.get('ContactNo', '')).lower() or
                    search_lower in str(resident.get('Address', '')).lower()):
                filtered.append(resident)

        return filtered