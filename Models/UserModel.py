"""
Models/UserModel.py
User authentication and management model
"""
from Models.Database import Database
from mysql.connector import Error
import hashlib


def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


class UserModel:
    """Handles all user-related database operations"""

    def __init__(self, db: Database):
        self.db = db

    def authenticate_user(self, username: str, password: str):
        """Authenticate resident user credentials"""
        if not self.db.connect():
            return None, "Database connection failed"

        try:
            cursor = self.db.connection.cursor(dictionary=True)

            query = """
                SELECT u.UserID,
                       u.Username,
                       u.UserType,
                       u.IsActive,
                       r.ResidentID,
                       r.RFirstName,
                       r.RMiddleName,
                       r.RLastName,
                       r.Sex,
                       r.ContactNo,
                       r.Address
                FROM users u
                INNER JOIN residents r ON u.UserID = r.UserID
                WHERE u.Username = %s
                  AND u.Password = %s
                  AND u.UserType = 'Resident'
                  AND u.IsActive = TRUE
            """
            cursor.execute(query, (username, hash_password(password)))
            result = cursor.fetchone()

            cursor.close()
            self.db.disconnect()

            if result:
                return result, None
            else:
                return None, "Invalid credentials or account is not active"

        except Error as e:
            self.db.disconnect()
            return None, f"Authentication error: {str(e)}"

    def authenticate_admin(self, username: str, password: str):
        """Authenticate admin credentials"""
        if not self.db.connect():
            return None, "Database connection failed"

        try:
            cursor = self.db.connection.cursor(dictionary=True)

            query = """
                SELECT u.UserID,
                       u.Username,
                       u.UserType,
                       u.IsActive,
                       a.AdminID,
                       a.AFirstName,
                       a.ALastName,
                       a.Role
                FROM users u
                INNER JOIN admins a ON u.UserID = a.UserID
                WHERE u.Username = %s
                  AND u.Password = %s
                  AND u.UserType = 'Admin'
                  AND u.IsActive = TRUE
            """
            cursor.execute(query, (username, hash_password(password)))
            result = cursor.fetchone()

            cursor.close()
            self.db.disconnect()

            if result:
                return result, None
            else:
                return None, "Invalid admin credentials or account is not active"

        except Error as e:
            self.db.disconnect()
            return None, f"Authentication error: {str(e)}"

    def register_user(self, username: str, password: str, first_name: str, middle_name: str,
                     last_name: str, sex: str, contact_no: str, address: str = None):
        """Register a new resident user"""
        if not self.db.connect():
            return False, "Database connection failed"

        try:
            cursor = self.db.connection.cursor()

            # Check if username already exists FIRST before generating IDs
            cursor.execute("SELECT UserID FROM users WHERE Username = %s", (username,))
            if cursor.fetchone():
                cursor.close()
                self.db.disconnect()
                return False, "Username already exists"

            # Generate new UserID using MAX to avoid ordering issues
            cursor.execute("SELECT MAX(CAST(SUBSTRING(UserID, 2) AS UNSIGNED)) as max_id FROM users")
            result = cursor.fetchone()
            next_user_num = (result[0] or 0) + 1
            new_user_id = f"U{str(next_user_num).zfill(3)}"

            # Generate new ResidentID using MAX
            cursor.execute("SELECT MAX(CAST(SUBSTRING(ResidentID, 2) AS UNSIGNED)) as max_id FROM residents")
            result = cursor.fetchone()
            next_resident_num = (result[0] or 0) + 1
            new_resident_id = f"R{str(next_resident_num).zfill(3)}"

            # Insert into users table with hashed password
            user_query = """
                INSERT INTO users (UserID, Username, Password, UserType, IsActive)
                VALUES (%s, %s, %s, 'Resident', TRUE)
            """
            cursor.execute(user_query, (new_user_id, username, hash_password(password)))

            # Insert into residents table with separate name fields
            resident_query = """
                INSERT INTO residents (ResidentID, UserID, RFirstName, RMiddleName, RLastName,
                                      Sex, ContactNo, Address)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(resident_query, (
                new_resident_id, new_user_id,
                first_name, middle_name or None, last_name,
                sex, contact_no, address
            ))

            self.db.connection.commit()
            cursor.close()
            self.db.disconnect()
            return True, "Registration successful"

        except Error as e:
            if self.db.connection:
                self.db.connection.rollback()
            self.db.disconnect()
            return False, f"Registration error: {str(e)}"

    def get_user_by_username(self, username: str):
        """Get user information by username"""
        if not self.db.connect():
            return None, "Database connection failed"

        try:
            cursor = self.db.connection.cursor(dictionary=True)

            query = """
                SELECT UserID, Username, UserType, IsActive
                FROM users
                WHERE Username = %s
            """
            cursor.execute(query, (username,))
            result = cursor.fetchone()

            cursor.close()
            self.db.disconnect()

            if result:
                return result, None
            else:
                return None, "User not found"

        except Error as e:
            self.db.disconnect()
            return None, f"Query error: {str(e)}"

    def check_username_exists(self, username: str) -> bool:
        """Check if username already exists in database"""
        user, error = self.get_user_by_username(username)
        return user is not None