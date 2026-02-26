"""
Models/PaymentModel.py
Payment data operations
"""
from Models.Database import Database
from mysql.connector import Error
from datetime import datetime
import random
import string


class PaymentModel:
    """Handles all payment-related database operations"""

    def __init__(self, db: Database):
        self.db = db

    def generate_receipt_number(self) -> str:
        """Generate unique receipt number"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        return f"RCPT-{timestamp}-{random_suffix}"

    def save_payment(self, violation_id: str, payment_type: str, amount: float,
                    payer_name: str, contact: str, reference: str = None):
        """Save payment to database"""
        if not self.db.connect():
            return False, "Database connection failed"

        try:
            cursor = self.db.connection.cursor()

            # Generate receipt number
            receipt_no = self.generate_receipt_number()

            # Get next PaymentID
            cursor.execute("SELECT PaymentID FROM payments ORDER BY PaymentID DESC LIMIT 1")
            last_payment = cursor.fetchone()
            if last_payment:
                last_num = int(last_payment[0][1:])
                new_payment_id = f"P{str(last_num + 1).zfill(3)}"
            else:
                new_payment_id = "P001"

            # Check if payment already exists for this violation
            cursor.execute(
                "SELECT PaymentID FROM payments WHERE ViolationID = %s",
                (violation_id,)
            )
            existing_payment = cursor.fetchone()

            if existing_payment:
                # Update existing payment
                query = """
                    UPDATE payments
                    SET Status = 'PAID',
                        PaymentType = %s,
                        AmountPaid = %s,
                        PaymentDate = NOW(),
                        ReceiptNo = %s
                    WHERE ViolationID = %s
                """
                cursor.execute(query, (payment_type, amount, receipt_no, violation_id))
            else:
                # Insert new payment
                query = """
                    INSERT INTO payments
                    (PaymentID, ViolationID, PaymentType, ReceiptNo, AmountPaid, PaymentDate, Status)
                    VALUES (%s, %s, %s, %s, %s, NOW(), 'PAID')
                """
                cursor.execute(query, (new_payment_id, violation_id, payment_type,
                                      receipt_no, amount))

            self.db.connection.commit()
            cursor.close()
            self.db.disconnect()

            return True, {
                'violation_id': violation_id,
                'receipt_no': receipt_no,
                'amount': amount,
                'payment_type': payment_type,
                'payer_name': payer_name,
                'contact': contact
            }

        except Exception as e:
            print(f"Payment save error: {e}")
            if self.db.connection:
                self.db.connection.rollback()
            self.db.disconnect()
            return False, str(e)

    def get_payment_history(self, resident_id: str):
        """Load payment history for a resident"""
        if not self.db.connect():
            return []

        try:
            cursor = self.db.connection.cursor(dictionary=True)

            query = """
                SELECT p.PaymentID,
                       p.ViolationID,
                       p.PaymentType,
                       p.AmountPaid,
                       DATE_FORMAT(p.PaymentDate, '%Y-%m-%d') as payment_date,
                       p.ReceiptNo
                FROM payments p
                INNER JOIN violations v ON p.ViolationID = v.ViolationID
                INNER JOIN vehicles vh ON v.VehicleID = vh.VehicleID
                WHERE vh.ResidentID = %s
                  AND p.Status = 'PAID'
                ORDER BY p.PaymentDate DESC
            """
            cursor.execute(query, (resident_id,))
            results = cursor.fetchall()

            cursor.close()
            self.db.disconnect()

            return results

        except Exception as e:
            print(f"Payment history error: {e}")
            self.db.disconnect()
            return []

    def get_all_payment_history(self, limit: int = 10):
        """Get recent payment history (for admin)"""
        if not self.db.connect():
            return []

        try:
            cursor = self.db.connection.cursor(dictionary=True)

            query = """
                SELECT p.PaymentID,
                       v.ViolationID,
                       CONCAT(r.RFirstName, ' ', r.RLastName) as resident_name,
                       vt.ViolationName,
                       vt.FineAmount,
                       DATE_FORMAT(p.PaymentDate, '%Y-%m-%d') as payment_date
                FROM payments p
                INNER JOIN violations v ON p.ViolationID = v.ViolationID
                INNER JOIN vehicles vh ON v.VehicleID = vh.VehicleID
                INNER JOIN residents r ON vh.ResidentID = r.ResidentID
                INNER JOIN violation_types vt ON v.ViolationTypeID = vt.ViolationTypeID
                WHERE p.Status = 'PAID'
                  AND v.IsDeleted = 0
                ORDER BY p.PaymentDate DESC LIMIT %s
            """
            cursor.execute(query, (limit,))
            results = cursor.fetchall()

            cursor.close()
            self.db.disconnect()

            return results

        except Exception as e:
            print(f"Payment history error: {e}")
            self.db.disconnect()
            return []

    def get_payment_statistics(self):
        """Get payment statistics for admin dashboard"""
        if not self.db.connect():
            return {
                'total_violations': 0,
                'paid_count': 0,
                'unpaid_count': 0,
                'total_revenue': 0.0,
                'pending_revenue': 0.0
            }

        try:
            cursor = self.db.connection.cursor(dictionary=True)

            query = """
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
            cursor.execute(query)
            results = cursor.fetchall()

            cursor.close()
            self.db.disconnect()

            total_violations = len(results)
            paid_count = sum(1 for v in results if v['PaymentStatus'] == 'PAID')
            unpaid_count = total_violations - paid_count
            total_revenue = sum(float(v['FineAmount']) for v in results if v['PaymentStatus'] == 'PAID')
            pending_revenue = sum(float(v['FineAmount']) for v in results if v['PaymentStatus'] != 'PAID')

            return {
                'total_violations': total_violations,
                'paid_count': paid_count,
                'unpaid_count': unpaid_count,
                'total_revenue': total_revenue,
                'pending_revenue': pending_revenue
            }

        except Exception as e:
            print(f"Payment stats error: {e}")
            self.db.disconnect()
            return {
                'total_violations': 0,
                'paid_count': 0,
                'unpaid_count': 0,
                'total_revenue': 0.0,
                'pending_revenue': 0.0
            }