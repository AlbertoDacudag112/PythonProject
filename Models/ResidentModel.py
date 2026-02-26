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
        """Load all residents with statistics — returns separate name fields"""
        if not self.db.connect():
            return []

        try:
            cursor = self.db.connection.cursor(dictionary=True)

            query = """
                SELECT r.ResidentID,
                       r.RFirstName as first_name,
                       COALESCE(r.RMiddleName, '') as middle_name,
                       r.RLastName as last_name,
                       r.Sex,
                       r.ContactNo,
                       r.Address,
                       COUNT(v.ViolationID) as total_violations
                FROM residents r
                LEFT JOIN vehicles vh ON r.ResidentID = vh.ResidentID
                LEFT JOIN violations v ON vh.VehicleID = v.VehicleID AND v.IsDeleted = 0
                GROUP BY r.ResidentID, r.RFirstName, r.RMiddleName, r.RLastName,
                         r.Sex, r.ContactNo, r.Address
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
        """Get detailed resident information with separate name fields and statistics"""
        if not self.db.connect():
            return None

        try:
            cursor = self.db.connection.cursor(dictionary=True)

            query = """
                SELECT r.ResidentID,
                       r.RFirstName as first_name,
                       COALESCE(r.RMiddleName, '') as middle_name,
                       r.RLastName as last_name,
                       r.Sex,
                       r.ContactNo,
                       r.Address,
                       COUNT(DISTINCT vh.VehicleID) as vehicle_count,
                       COUNT(DISTINCT v.ViolationID) as violation_count,
                       SUM(CASE WHEN v.ViolationID IS NOT NULL AND p.Status = 'PAID' THEN 1 ELSE 0 END) as paid_count,
                       SUM(CASE WHEN v.ViolationID IS NOT NULL AND (p.Status IS NULL OR p.Status != 'PAID') THEN 1 ELSE 0 END) as unpaid_count
                FROM residents r
                LEFT JOIN vehicles vh ON r.ResidentID = vh.ResidentID
                LEFT JOIN violations v ON vh.VehicleID = v.VehicleID AND v.IsDeleted = 0
                LEFT JOIN payments p ON v.ViolationID = p.ViolationID
                WHERE r.ResidentID = %s
                GROUP BY r.ResidentID, r.RFirstName, r.RMiddleName, r.RLastName,
                         r.Sex, r.ContactNo, r.Address
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
        """Get residents formatted for dropdown — returns separate name fields"""
        if not self.db.connect():
            return []

        try:
            cursor = self.db.connection.cursor(dictionary=True)
            query = """
                SELECT ResidentID,
                       RFirstName as first_name,
                       COALESCE(RMiddleName, '') as middle_name,
                       RLastName as last_name
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