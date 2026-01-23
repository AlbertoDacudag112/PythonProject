"""
Models/ResidentModel.py
Resident data operations
"""
from Models.Database import Database
from mysql.connector import Error


class ResidentModel:
    """Handles all resident-related database operations"""

    def __init__(self, db: Database):
        self.db = db

    def get_all_residents(self):
        """Load all residents with statistics"""
        if not self.db.connect():
            return []

        try:
            cursor = self.db.connection.cursor(dictionary=True)

            query = """
                SELECT r.ResidentID,
                       CONCAT(r.RFirstName, ' ', COALESCE(r.RMiddleName, ''), ' ', r.RLastName) as full_name,
                       r.Sex,
                       r.ContactNo,
                       r.Address,
                       COUNT(v.ViolationID) as total_violations
                FROM residents r
                LEFT JOIN vehicles vh ON r.ResidentID = vh.ResidentID
                LEFT JOIN violations v ON vh.VehicleID = v.VehicleID
                GROUP BY r.ResidentID
                ORDER BY r.ResidentID
            """
            cursor.execute(query)
            results = cursor.fetchall()

            cursor.close()
            self.db.disconnect()

            return results

        except Exception as e:
            print(f"Load residents error: {e}")
            self.db.disconnect()
            return []

    def get_resident_details(self, resident_id: str):
        """Get detailed resident information with statistics"""
        if not self.db.connect():
            return None

        try:
            cursor = self.db.connection.cursor(dictionary=True)

            # Get resident info
            query = """
                SELECT r.ResidentID,
                       CONCAT(r.RFirstName, ' ', COALESCE(r.RMiddleName, ''), ' ', r.RLastName) as full_name,
                       r.Sex,
                       r.ContactNo,
                       r.Address,
                       COUNT(DISTINCT vh.VehicleID) as vehicle_count,
                       COUNT(v.ViolationID) as violation_count,
                       SUM(CASE WHEN COALESCE(p.Status, 'UNPAID') = 'PAID' THEN 1 ELSE 0 END) as paid_count,
                       SUM(CASE WHEN COALESCE(p.Status, 'UNPAID') = 'UNPAID' THEN 1 ELSE 0 END) as unpaid_count
                FROM residents r
                LEFT JOIN vehicles vh ON r.ResidentID = vh.ResidentID
                LEFT JOIN violations v ON vh.VehicleID = v.VehicleID
                LEFT JOIN payments p ON v.ViolationID = p.ViolationID
                WHERE r.ResidentID = %s
                GROUP BY r.ResidentID
            """
            cursor.execute(query, (resident_id,))
            result = cursor.fetchone()

            cursor.close()
            self.db.disconnect()

            return result

        except Exception as e:
            print(f"Get resident details error: {e}")
            self.db.disconnect()
            return None

    def get_resident_vehicles(self, resident_id: str):
        """Get all vehicles registered to a resident"""
        if not self.db.connect():
            return []

        try:
            cursor = self.db.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT PlateNo, Brand, Model
                FROM vehicles
                WHERE ResidentID = %s
            """, (resident_id,))
            vehicles = cursor.fetchall()

            cursor.close()
            self.db.disconnect()

            return vehicles

        except Exception as e:
            print(f"Get resident vehicles error: {e}")
            self.db.disconnect()
            return []

    def get_total_residents(self):
        """Get total number of residents"""
        if not self.db.connect():
            return 0

        try:
            cursor = self.db.connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM residents")
            result = cursor.fetchone()
            cursor.close()
            self.db.disconnect()
            return result[0] if result else 0
        except:
            self.db.disconnect()
            return 0

    def get_residents_for_dropdown(self):
        """Get residents formatted for dropdown/combobox"""
        if not self.db.connect():
            return []

        try:
            cursor = self.db.connection.cursor(dictionary=True)
            query = """
                SELECT ResidentID, 
                       CONCAT(RFirstName, ' ', RLastName) as full_name
                FROM residents
                ORDER BY RFirstName, RLastName
            """
            cursor.execute(query)
            results = cursor.fetchall()

            cursor.close()
            self.db.disconnect()

            return results

        except Exception as e:
            print(f"Load residents error: {e}")
            self.db.disconnect()
            return []