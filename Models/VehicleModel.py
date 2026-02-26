"""
Models/VehicleModel.py
Vehicle data operations
"""
from Models.Database import Database
from mysql.connector import Error


class VehicleModel:
    """Handles all vehicle-related database operations"""

    def __init__(self, db: Database):
        self.db = db

    def get_all_vehicles(self):
        """Load all vehicles with owner and violation count"""
        if not self.db.connect():
            return []

        try:
            cursor = self.db.connection.cursor(dictionary=True)

            query = """
                SELECT vh.VehicleID,
                       vh.PlateNo,
                       CONCAT(r.RFirstName, ' ', r.RLastName) as owner_name,
                       vh.Brand,
                       vh.Model,
                       COUNT(CASE WHEN v.IsDeleted = 0 THEN v.ViolationID END) as violations
                FROM vehicles vh
                INNER JOIN residents r ON vh.ResidentID = r.ResidentID
                LEFT JOIN violations v ON vh.VehicleID = v.VehicleID
                GROUP BY vh.VehicleID
                ORDER BY vh.VehicleID
            """
            cursor.execute(query)
            results = cursor.fetchall()

            cursor.close()
            self.db.disconnect()

            return results

        except Exception as e:
            print(f"Load vehicles error: {e}")
            self.db.disconnect()
            return []

    def get_vehicle_by_id(self, vehicle_id: str):
        """Get vehicle details by ID - FIXED: Added ResidentID"""
        if not self.db.connect():
            return None

        try:
            cursor = self.db.connection.cursor(dictionary=True)
            query = """
                SELECT vh.VehicleID,
                       vh.ResidentID,
                       vh.PlateNo,
                       vh.Brand,
                       vh.Model,
                       vh.Color,
                       CONCAT(r.RFirstName, ' ', r.RLastName) as owner_name
                FROM vehicles vh
                INNER JOIN residents r ON vh.ResidentID = r.ResidentID
                WHERE vh.VehicleID = %s
            """
            cursor.execute(query, (vehicle_id,))
            result = cursor.fetchone()

            cursor.close()
            self.db.disconnect()

            return result

        except Exception as e:
            print(f"Get vehicle error: {e}")
            self.db.disconnect()
            return None

    def add_vehicle(self, resident_id: str, plate_no: str, brand: str, model: str, color: str = None):
        """Add new vehicle to database"""
        if not self.db.connect():
            return False, "Database connection failed"

        try:
            cursor = self.db.connection.cursor()

            # Check if plate number already exists
            cursor.execute("SELECT VehicleID FROM vehicles WHERE PlateNo = %s", (plate_no,))
            if cursor.fetchone():
                cursor.close()
                self.db.disconnect()
                return False, "This plate number is already registered"

            # Generate new VehicleID
            cursor.execute("SELECT VehicleID FROM vehicles ORDER BY VehicleID DESC LIMIT 1")
            last_vehicle = cursor.fetchone()
            if last_vehicle:
                last_num = int(last_vehicle[0][2:])
                new_vehicle_id = f"VH{str(last_num + 1).zfill(3)}"
            else:
                new_vehicle_id = "VH001"

            # Insert vehicle
            query = """
                INSERT INTO vehicles (VehicleID, ResidentID, PlateNo, Brand, Model, Color)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (new_vehicle_id, resident_id, plate_no, brand, model, color))

            self.db.connection.commit()
            cursor.close()
            self.db.disconnect()

            return True, "Vehicle registered successfully"

        except Exception as e:
            if self.db.connection:
                self.db.connection.rollback()
            self.db.disconnect()
            return False, f"Failed to register vehicle: {str(e)}"

    def update_vehicle(self, vehicle_id: str, brand: str, model: str, color: str = None):
        """Update vehicle information (plate number cannot be changed)"""
        if not self.db.connect():
            return False, "Database connection failed"

        try:
            cursor = self.db.connection.cursor()

            # Update vehicle (plate number is NOT updated)
            query = """
                UPDATE vehicles
                SET Brand = %s, Model = %s, Color = %s
                WHERE VehicleID = %s
            """
            cursor.execute(query, (brand, model, color, vehicle_id))

            self.db.connection.commit()
            cursor.close()
            self.db.disconnect()

            return True, "Vehicle updated successfully"

        except Exception as e:
            if self.db.connection:
                self.db.connection.rollback()
            self.db.disconnect()
            return False, f"Failed to update vehicle: {str(e)}"

    def get_total_vehicles(self):
        """Get total number of vehicles"""
        if not self.db.connect():
            return 0

        try:
            cursor = self.db.connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM vehicles")
            result = cursor.fetchone()
            cursor.close()
            self.db.disconnect()
            return result[0] if result else 0
        except:
            self.db.disconnect()
            return 0

    def get_vehicles_for_dropdown(self):
        """Get vehicles formatted for dropdown/combobox"""
        if not self.db.connect():
            return []

        try:
            cursor = self.db.connection.cursor(dictionary=True)
            query = """
                SELECT v.VehicleID,
                       v.PlateNo,
                       CONCAT(r.RFirstName, ' ', r.RLastName) as owner_name
                FROM vehicles v
                INNER JOIN residents r ON v.ResidentID = r.ResidentID
                ORDER BY v.PlateNo
            """
            cursor.execute(query)
            results = cursor.fetchall()

            cursor.close()
            self.db.disconnect()

            return results

        except Exception as e:
            print(f"Load vehicles error: {e}")
            self.db.disconnect()
            return []