"""
Models/ReportModel.py
Report generation data operations
"""
from Models.Database import Database
from mysql.connector import Error


class ReportModel:
    """Handles all report-related database queries"""

    def __init__(self, db: Database):
        self.db = db

    def get_violations_report_data(self):
        """Get all violations data for report generation"""
        if not self.db.connect():
            return []

        try:
            cursor = self.db.connection.cursor(dictionary=True)
            query = """
                SELECT v.ViolationID,
                       CONCAT(r.RFirstName, ' ', r.RLastName) as ResidentName,
                       r.ContactNo,
                       vh.PlateNo,
                       vh.Brand,
                       vh.Model,
                       vt.ViolationName,
                       vt.FineAmount,
                       DATE_FORMAT(v.ViolationDate, '%Y-%m-%d') as ViolationDate,
                       COALESCE(p.Status, 'UNPAID') as PaymentStatus,
                       DATE_FORMAT(p.PaymentDate, '%Y-%m-%d') as PaymentDate
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
            print(f"Report data error: {e}")
            self.db.disconnect()
            return []

    def get_payment_report_statistics(self):
        """Get payment statistics for reports"""
        if not self.db.connect():
            return None

        try:
            cursor = self.db.connection.cursor(dictionary=True)

            # Get ALL violations data (same query as violations report)
            violations_query = """
                SELECT v.ViolationID,
                       vt.FineAmount,
                       COALESCE(p.Status, 'UNPAID') as PaymentStatus
                FROM violations v
                INNER JOIN vehicles vh ON v.VehicleID = vh.VehicleID
                INNER JOIN residents r ON vh.ResidentID = r.ResidentID
                INNER JOIN violation_types vt ON v.ViolationTypeID = vt.ViolationTypeID
                LEFT JOIN payments p ON v.ViolationID = p.ViolationID
                WHERE v.IsDeleted = 0
            """
            cursor.execute(violations_query)
            all_violations = cursor.fetchall()

            cursor.close()
            self.db.disconnect()

            # Calculate statistics from actual data
            total_violations = len(all_violations)
            paid_count = sum(1 for v in all_violations if v['PaymentStatus'] == 'PAID')
            unpaid_count = total_violations - paid_count
            total_revenue = sum(float(v['FineAmount']) for v in all_violations if v['PaymentStatus'] == 'PAID')
            pending_revenue = sum(float(v['FineAmount']) for v in all_violations if v['PaymentStatus'] != 'PAID')

            return {
                'total_violations': total_violations,
                'paid_count': paid_count,
                'unpaid_count': unpaid_count,
                'total_revenue': total_revenue,
                'pending_revenue': pending_revenue
            }

        except Exception as e:
            print(f"Payment report stats error: {e}")
            self.db.disconnect()
            return None