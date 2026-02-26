"""
Models/ViolationModel.py
Violation data operations
"""
from Models.Database import Database
from mysql.connector import Error


class ViolationModel:
    """Handles all violation-related database operations"""

    def __init__(self, db: Database):
        self.db = db

    def get_user_violations(self, resident_id: str):
        """Get all violations for a specific resident"""
        if not self.db.connect():
            return []

        try:
            cursor = self.db.connection.cursor(dictionary=True)

            query = """
                SELECT v.ViolationID as violation_id,
                       vh.PlateNo as plate_no,
                       vt.ViolationName as violation_type,
                       DATE_FORMAT(v.ViolationDate, '%Y-%m-%d') as date,
                       vt.FineAmount as fine_amount,
                       COALESCE(p.Status, 'UNPAID') as status
                FROM violations v
                INNER JOIN vehicles vh ON v.VehicleID = vh.VehicleID
                INNER JOIN violation_types vt ON v.ViolationTypeID = vt.ViolationTypeID
                LEFT JOIN payments p ON v.ViolationID = p.ViolationID
                WHERE vh.ResidentID = %s
                  AND v.IsDeleted = 0
                ORDER BY v.ViolationDate DESC
            """
            cursor.execute(query, (resident_id,))
            results = cursor.fetchall()

            cursor.close()
            self.db.disconnect()

            # Convert status to simpler format for display
            for result in results:
                if result['status'] == 'PAID':
                    result['status'] = 'Paid'
                else:
                    result['status'] = 'Unpaid'

            return results

        except Exception as e:
            print(f"Violations query error: {e}")
            self.db.disconnect()
            return []

    def get_all_violations(self):
        """Get all violations (for admin view)"""
        if not self.db.connect():
            return []

        try:
            cursor = self.db.connection.cursor(dictionary=True)

            query = """
                SELECT v.ViolationID,
                       CONCAT(r.RFirstName, ' ', r.RLastName) as resident_name,
                       vh.PlateNo,
                       vt.ViolationName,
                       DATE_FORMAT(v.ViolationDate, '%Y-%m-%d') as date,
                       vt.FineAmount,
                       COALESCE(p.Status, 'UNPAID') as status,
                       v.IsDeleted
                FROM violations v
                INNER JOIN vehicles vh ON v.VehicleID = vh.VehicleID
                INNER JOIN residents r ON vh.ResidentID = r.ResidentID
                INNER JOIN violation_types vt ON v.ViolationTypeID = vt.ViolationTypeID
                LEFT JOIN payments p ON v.ViolationID = p.ViolationID
                WHERE v.IsDeleted = 0
                ORDER BY v.ViolationDate DESC
            """
            cursor.execute(query)
            results = cursor.fetchall()

            cursor.close()
            self.db.disconnect()

            return results

        except Exception as e:
            print(f"All violations query error: {e}")
            self.db.disconnect()
            return []

    def get_violation_by_id(self, violation_id: str):
        """Get detailed violation information"""
        if not self.db.connect():
            return None

        try:
            cursor = self.db.connection.cursor(dictionary=True)

            query = """
                SELECT v.ViolationID,
                       CONCAT(r.RFirstName, ' ', r.RLastName) as resident_name,
                       r.ContactNo,
                       vh.PlateNo,
                       vh.Brand,
                       vh.Model,
                       vt.ViolationName,
                       vt.FineAmount,
                       DATE_FORMAT(v.ViolationDate, '%Y-%m-%d') as ViolationDate,
                       COALESCE(p.Status, 'UNPAID') as status,
                       DATE_FORMAT(p.PaymentDate, '%Y-%m-%d') as PaymentDate
                FROM violations v
                INNER JOIN vehicles vh ON v.VehicleID = vh.VehicleID
                INNER JOIN residents r ON vh.ResidentID = r.ResidentID
                INNER JOIN violation_types vt ON v.ViolationTypeID = vt.ViolationTypeID
                LEFT JOIN payments p ON v.ViolationID = p.ViolationID
                WHERE v.ViolationID = %s
            """
            cursor.execute(query, (violation_id,))
            result = cursor.fetchone()

            cursor.close()
            self.db.disconnect()

            return result

        except Exception as e:
            print(f"Violation details query error: {e}")
            self.db.disconnect()
            return None

    def add_violation(self, vehicle_id: str, violation_type_id: str, violation_date: str):
        """Add new violation to database"""
        if not self.db.connect():
            return False, "Database connection failed"

        try:
            cursor = self.db.connection.cursor()

            # Generate new ViolationID
            cursor.execute("SELECT MAX(CAST(SUBSTRING(ViolationID, 2) AS UNSIGNED)) as max_id FROM violations")
            result = cursor.fetchone()

            if result and result[0]:
                new_num = int(result[0]) + 1
            else:
                new_num = 1

            new_violation_id = f"V{str(new_num).zfill(3)}"

            # Insert violation
            query = """
                INSERT INTO violations (ViolationID, VehicleID, ViolationTypeID, ViolationDate, IsDeleted)
                VALUES (%s, %s, %s, %s, 0)
            """
            cursor.execute(query, (new_violation_id, vehicle_id, violation_type_id, violation_date))

            self.db.connection.commit()
            cursor.close()
            self.db.disconnect()

            return True, "Violation added successfully"

        except Exception as e:
            if self.db.connection:
                self.db.connection.rollback()
            self.db.disconnect()
            return False, f"Failed to add violation: {str(e)}"

    def get_violation_statistics(self, resident_id: str = None):
        """Get violation statistics"""
        if not self.db.connect():
            return 0, 0

        try:
            cursor = self.db.connection.cursor(dictionary=True)

            if resident_id:
                # Get statistics for specific resident
                query = """
                    SELECT v.ViolationID,
                           COALESCE(p.Status, 'UNPAID') as status
                    FROM violations v
                    INNER JOIN vehicles vh ON v.VehicleID = vh.VehicleID
                    LEFT JOIN payments p ON v.ViolationID = p.ViolationID
                    WHERE vh.ResidentID = %s
                      AND v.IsDeleted = 0
                """
                cursor.execute(query, (resident_id,))
            else:
                # Get all statistics (for admin)
                query = """
                    SELECT v.ViolationID,
                           COALESCE(p.Status, 'UNPAID') as status
                    FROM violations v
                    LEFT JOIN payments p ON v.ViolationID = p.ViolationID
                    WHERE v.IsDeleted = 0
                """
                cursor.execute(query)

            results = cursor.fetchall()

            cursor.close()
            self.db.disconnect()

            total_violations = len(results)
            unpaid_violations = sum(1 for v in results if v['status'] != 'PAID')

            return total_violations, unpaid_violations

        except Exception as e:
            print(f"Stats error: {e}")
            self.db.disconnect()
            return 0, 0

    def get_monthly_violations(self, resident_id: str = None, year: int = None):
        """Get violations grouped by month, optionally filtered by year"""
        if not self.db.connect():
            return {}

        try:
            import datetime
            filter_year = year if year else datetime.date.today().year
            cursor = self.db.connection.cursor()

            if resident_id:
                query = """
                    SELECT DATE_FORMAT(v.ViolationDate, '%b') as month, COUNT(*) as count
                    FROM violations v
                    INNER JOIN vehicles vh ON v.VehicleID = vh.VehicleID
                    WHERE vh.ResidentID = %s
                      AND YEAR(v.ViolationDate) = %s
                      AND v.IsDeleted = 0
                    GROUP BY MONTH(v.ViolationDate), DATE_FORMAT(v.ViolationDate, '%b')
                    ORDER BY MONTH(v.ViolationDate)
                """
                cursor.execute(query, (resident_id, filter_year))
            else:
                query = """
                    SELECT DATE_FORMAT(ViolationDate, '%b') as month, COUNT(*) as count
                    FROM violations
                    WHERE YEAR(ViolationDate) = %s
                      AND IsDeleted = 0
                    GROUP BY MONTH(ViolationDate), DATE_FORMAT(ViolationDate, '%b')
                    ORDER BY MONTH(ViolationDate)
                """
                cursor.execute(query, (filter_year,))

            results = cursor.fetchall()

            cursor.close()
            self.db.disconnect()

            # Create dictionary with all months
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            monthly_data = {month: 0 for month in months}

            # Fill in actual data
            for month, count in results:
                monthly_data[month] = count

            return monthly_data

        except Exception as e:
            print(f"Monthly data error: {e}")
            self.db.disconnect()
            return {month: 0 for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']}

    def get_violation_types(self):
        """Get all violation types"""
        if not self.db.connect():
            return []

        try:
            cursor = self.db.connection.cursor(dictionary=True)
            query = "SELECT ViolationTypeID, ViolationName, FineAmount FROM violation_types ORDER BY ViolationName"
            cursor.execute(query)
            results = cursor.fetchall()

            cursor.close()
            self.db.disconnect()

            return results

        except Exception as e:
            print(f"Load violation types error: {e}")
            self.db.disconnect()
            return []