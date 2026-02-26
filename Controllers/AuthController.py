"""
Controllers/AuthController.py
Authentication and registration business logic (extracted from RoadEyeMain.py and SignUpWindow.py)
"""
from Models.Database import Database
from Models.UserModel import UserModel
from Controllers.Utility.ValidationHelper import ValidationHelper


class AuthController:
    """Handles authentication and registration business logic"""

    def __init__(self):
        self.db = Database(host='localhost', database='RoadEyeDB', user='root', password='')
        self.user_model = UserModel(self.db)

    def login(self, username: str, password: str):
        """
        Process login attempt for both admin and resident users

        Args:
            username: User's username
            password: User's password

        Returns:
            tuple: (user_data_dict, error_message)
                   user_data_dict will be None if login fails
        """
        # Validate input
        if not username or not password:
            return None, "Please enter both username and password"

        # Try admin authentication first
        admin, admin_error = self.user_model.authenticate_admin(username, password)
        if admin:
            self.db.log_activity(admin['UserID'], f"Admin login: {username}")
            admin['user_type'] = 'admin'  # Add type identifier
            return admin, None

        # Try resident authentication
        user, user_error = self.user_model.authenticate_user(username, password)
        if user:
            self.db.log_activity(user['UserID'], f"User login: {username}")
            user['user_type'] = 'resident'  # Add type identifier
            return user, None

        # Generic error for security
        return None, "Invalid username or password"

    def register(self, form_data: dict):
        """
        Process user registration

        Args:
            form_data: Dictionary containing registration form data
                Required keys: username, password, confirm_password, first_name,
                              last_name, sex, contact_no
                Optional keys: middle_name, address

        Returns:
            tuple: (success: bool, message: str)
        """
        # Validate all fields
        validation_errors = self._validate_registration_data(form_data)
        if validation_errors:
            return False, "\n".join(validation_errors)

        # Register user
        success, message = self.user_model.register_user(
            username=form_data['username'],
            password=form_data['password'],
            first_name=form_data['first_name'],
            middle_name=form_data.get('middle_name'),
            last_name=form_data['last_name'],
            sex=form_data['sex'],
            contact_no=form_data['contact_no'],
            address=form_data.get('address')
        )

        return success, message

    def check_username_exists(self, username: str) -> bool:
        """
        Check if username already exists in database

        Args:
            username: Username to check

        Returns:
            bool: True if username exists, False otherwise
        """
        return self.user_model.check_username_exists(username)

    def _validate_registration_data(self, data: dict) -> list:
        """
        Validate registration form data

        Args:
            data: Dictionary containing form data

        Returns:
            list: List of error messages (empty if all valid)
        """
        errors = []

        # Username validation
        is_valid, error = ValidationHelper.validate_username(data.get('username', ''))
        if not is_valid and error:
            errors.append(error)
        elif is_valid:
            # Check if username exists in database
            if self.check_username_exists(data.get('username', '')):
                errors.append("Username already exists. Please choose another.")

        # Password validation
        is_valid, error = ValidationHelper.validate_password(data.get('password', ''))
        if not is_valid and error:
            errors.append(error)

        # Confirm password validation
        is_valid, error = ValidationHelper.validate_confirm_password(
            data.get('password', ''),
            data.get('confirm_password', '')
        )
        if not is_valid and error:
            errors.append(error)

        # First name validation
        is_valid, error = ValidationHelper.validate_name(
            data.get('first_name', ''),
            "First name"
        )
        if not is_valid and error:
            errors.append(error)

        # Last name validation
        is_valid, error = ValidationHelper.validate_name(
            data.get('last_name', ''),
            "Last name"
        )
        if not is_valid and error:
            errors.append(error)

        # Contact number validation
        is_valid, error = ValidationHelper.validate_contact_number(
            data.get('contact_no', '')
        )
        if not is_valid and error:
            errors.append(error)

        return errors

    def logout(self, user_data: dict):
        """
        Process user logout

        Args:
            user_data: Dictionary containing user information with UserID and Username
        """
        user_type = user_data.get('user_type', 'User')
        username = user_data.get('Username', 'Unknown')
        user_id = user_data.get('UserID')

        if user_id:
            if user_type == 'admin':
                self.db.log_activity(user_id, f"Admin logout: {username}")
            else:
                self.db.log_activity(user_id, f"User logout: {username}")