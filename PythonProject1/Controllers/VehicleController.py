from Models.Database import Database
from Models.VehicleModel import VehicleModel


class VehicleController:
    """Handles vehicle management business logic"""

    def __init__(self):
        self.db = Database(host='localhost', database='RoadEyeDB', user='root', password='')
        self.vehicle_model = VehicleModel(self.db)

    def get_all_vehicles(self):
        """Get all vehicles"""
        return self.vehicle_model.get_all_vehicles()

    def get_vehicle_details(self, vehicle_id: str):
        """Get vehicle details"""
        return self.vehicle_model.get_vehicle_by_id(vehicle_id)

    def add_vehicle(self, resident_id: str, plate_no: str, brand: str, model: str, color: str = None):
        """
        Add new vehicle

        Returns:
            tuple: (success: bool, message: str)
        """
        # Validate inputs
        if not plate_no or not plate_no.strip():
            return False, "Please enter plate number"

        if not brand or not brand.strip():
            return False, "Please enter vehicle brand"

        if not model or not model.strip():
            return False, "Please enter vehicle model"

        return self.vehicle_model.add_vehicle(resident_id, plate_no, brand, model, color)

    def update_vehicle(self, vehicle_id: str, brand: str, model: str, color: str = None):
        """
        Update vehicle information

        Returns:
            tuple: (success: bool, message: str)
        """
        # Validate inputs
        if not brand or not brand.strip():
            return False, "Please enter vehicle brand"

        if not model or not model.strip():
            return False, "Please enter vehicle model"

        return self.vehicle_model.update_vehicle(vehicle_id, brand, model, color)

    def get_vehicles_for_dropdown(self):
        """Get vehicles formatted for dropdown"""
        return self.vehicle_model.get_vehicles_for_dropdown()

    def search_vehicles(self, vehicles: list, search_text: str):
        """
        Filter vehicles based on search text

        Args:
            vehicles: List of all vehicles
            search_text: Search query

        Returns:
            Filtered list of vehicles
        """
        if not search_text:
            return vehicles

        search_lower = search_text.lower()
        filtered = []

        for vehicle in vehicles:
            # Search across multiple fields
            if (search_lower in str(vehicle.get('VehicleID', '')).lower() or
                    search_lower in str(vehicle.get('PlateNo', '')).lower() or
                    search_lower in str(vehicle.get('owner_name', '')).lower() or
                    search_lower in str(vehicle.get('Brand', '')).lower() or
                    search_lower in str(vehicle.get('Model', '')).lower()):
                filtered.append(vehicle)

        return filtered