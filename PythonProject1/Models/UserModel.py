"""
Models/UserModel.py
User authentication and management model
"""
from Models.Database import Database
from mysql.connector import Error


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

            # Join users and residents tables to get complete user info
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
            cursor.execute(query, (username, password))
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

            # Join users and admins tables to get complete admin info
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
            cursor.execute(query, (username, password))
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

            # Generate new UserID and ResidentID
            # Get the last UserID
            cursor.execute("SELECT UserID FROM users ORDER BY UserID DESC LIMIT 1")
            last_user = cursor.fetchone()
            if last_user:
                last_num = int(last_user[0][1:])
                new_user_id = f"U{str(last_num + 1).zfill(3)}"
            else:
                new_user_id = "U024"

            # Get the last ResidentID
            cursor.execute("SELECT ResidentID FROM residents ORDER BY ResidentID DESC LIMIT 1")
            last_resident = cursor.fetchone()
            if last_resident:
                last_num = int(last_resident[0][1:])
                new_resident_id = f"R{str(last_num + 1).zfill(3)}"
            else:
                new_resident_id = "R021"

            # Check if username already exists
            cursor.execute("SELECT UserID FROM users WHERE Username = %s", (username,))
            if cursor.fetchone():
                cursor.close()
                self.db.disconnect()
                return False, "Username already exists"

            # Insert into users table
            user_query = """
                INSERT INTO users (UserID, Username, Password, UserType, IsActive)
                VALUES (%s, %s, %s, 'Resident', TRUE)
            """
            cursor.execute(user_query, (new_user_id, username, password))

            # Insert into residents table
            resident_query = """
                INSERT INTO residents (ResidentID, UserID, RFirstName, RMiddleName, RLastName, Sex,
                                      ContactNo, Address)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(resident_query, (new_resident_id, new_user_id, first_name, middle_name,
                                           last_name, sex, contact_no, address))

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