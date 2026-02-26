from Models.Database import Database
from Models.ViolationModel import ViolationModel


class ViolationController:
    """Handles violation management business logic"""

    def __init__(self):
        self.db = Database(host='localhost', database='RoadEyeDB', user='root', password='')
        self.violation_model = ViolationModel(self.db)

    def get_all_violations(self):
        """Get all violations (admin view)"""
        return self.violation_model.get_all_violations()

    def get_violation_details(self, violation_id: str):
        """Get detailed violation information"""
        return self.violation_model.get_violation_by_id(violation_id)

    def add_violation(self, vehicle_id: str, violation_type_id: str, violation_date: str):
        """Add new violation"""
        return self.violation_model.add_violation(vehicle_id, violation_type_id, violation_date)

    def get_violation_types(self):
        """Get all available violation types"""
        return self.violation_model.get_violation_types()

    def search_violations(self, violations: list, search_text: str):
        """
        Filter violations based on search text

        Args:
            violations: List of all violations
            search_text: Search query

        Returns:
            Filtered list of violations
        """
        if not search_text:
            return violations

        search_lower = search_text.lower()
        filtered = []

        for violation in violations:
            # Search across multiple fields
            if (search_lower in str(violation.get('ViolationID', '')).lower() or
                    search_lower in str(violation.get('resident_name', '')).lower() or
                    search_lower in str(violation.get('PlateNo', '')).lower() or
                    search_lower in str(violation.get('ViolationName', '')).lower()):
                filtered.append(violation)

        return filtered