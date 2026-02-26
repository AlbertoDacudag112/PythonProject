"""
Models/Database.py
Base Database connection class
"""
import mysql.connector
from mysql.connector import Error


class Database:
    """Database connection and operations handler"""

    def __init__(self, host='localhost', database='RoadEyeDB', user='root', password=''):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def connect(self):
        """Establish connection to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )

            if self.connection.is_connected():
                return True
        except Error as e:
            print(f"Database connection error: {e}")
            return False
        return False

    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def check_and_migrate(self):
        """Check if database needs migration and apply it"""
        if not self.connect():
            return False, "Database connection failed"

        try:
            cursor = self.connection.cursor()

            # Check if IsDeleted column exists in violations table
            cursor.execute("""
                SELECT COUNT(*)
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = %s
                  AND TABLE_NAME = 'violations'
                  AND COLUMN_NAME = 'IsDeleted'
            """, (self.database,))

            exists = cursor.fetchone()[0]

            if not exists:
                print("Applying database migration: Adding IsDeleted column...")
                cursor.execute("""
                    ALTER TABLE violations
                    ADD COLUMN IsDeleted TINYINT(1) DEFAULT 0
                """)
                cursor.execute("UPDATE violations SET IsDeleted = 0 WHERE IsDeleted IS NULL")
                self.connection.commit()
                print("✅ Migration completed successfully")

            cursor.close()
            self.disconnect()
            return True, "Database is up to date"

        except Error as e:
            if self.connection:
                self.connection.rollback()
            self.disconnect()
            return False, f"Migration error: {str(e)}"

    def log_activity(self, user_id, action, table_affected=None, record_id=None, ip_address=None):
        """Log user activity"""
        if not self.connect():
            return False

        try:
            cursor = self.connection.cursor()

            query = """
                INSERT INTO activity_logs (UserID, Action, TableAffected, RecordID, IPAddress)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (user_id, action, table_affected, record_id, ip_address))
            self.connection.commit()

            cursor.close()
            self.disconnect()
            return True

        except Error as e:
            self.disconnect()
            print(f"Activity log error: {e}")
            return False

    def get_violation_types_table_name(self):
        """Get the correct name of the violation types table"""
        if not self.connect():
            return None

        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SHOW TABLES LIKE '%violation%type%'")
            tables = cursor.fetchall()

            for table in tables:
                table_name = list(table.values())[0].lower()
                if 'violation' in table_name and 'type' in table_name:
                    actual_name = list(table.values())[0]
                    cursor.close()
                    self.disconnect()
                    return actual_name

            cursor.close()
            self.disconnect()
            return None
        except Error as e:
            print(f"Error finding violation types table: {e}")
            self.disconnect()
            return None